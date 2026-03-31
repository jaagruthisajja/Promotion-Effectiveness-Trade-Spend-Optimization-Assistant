from __future__ import annotations

from datetime import datetime, timezone


def _to_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)

    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _format_datetime(value: str | None) -> str:
    return _to_datetime(value).strftime("%d %b %Y, %I:%M %p")


def _format_time(value: str | None) -> str:
    return _to_datetime(value).strftime("%I:%M %p")


def _derive_message_task(subject: str) -> str:
    lowered = subject.lower()
    if "review" in lowered:
        return f"Review and respond: {subject}"
    if "confirm" in lowered:
        return f"Confirm requested item: {subject}"
    return f"Follow up on: {subject}"


def normalize_graph_snapshot(graph_data: dict) -> dict:
    employee = graph_data["me"]

    messages = [
        {
            "id": item["id"],
            "source": "Outlook",
            "sender": (((item.get("from") or {}).get("emailAddress")) or {}).get(
                "name", "Unknown"
            ),
            "subject": item.get("subject") or "(No subject)",
            "receivedAt": item.get("receivedDateTime"),
            "importance": item.get("importance", "normal"),
            "needsReply": not item.get("isRead", False)
            or bool((item.get("flag") or {}).get("flagStatus")),
            "extractedTask": _derive_message_task(item.get("subject") or "(No subject)"),
        }
        for item in graph_data.get("messages", [])
    ]

    messages.extend(
        {
            "id": f"chat-{item['id']}",
            "source": "Teams",
            "sender": item.get("from", "Unknown"),
            "subject": item.get("topic") or "Teams chat",
            "receivedAt": item.get("createdDateTime"),
            "importance": "medium",
            "needsReply": True,
            "extractedTask": item.get("preview")[:80] or "Follow up in Teams",
        }
        for item in graph_data.get("chatSignals", [])
    )

    meetings = [
        {
            "id": item["id"],
            "title": item.get("subject") or "Meeting",
            "start": (item.get("start") or {}).get("dateTime"),
            "end": (item.get("end") or {}).get("dateTime"),
            "location": ((item.get("location") or {}).get("displayName")) or "Online",
            "organizer": (
                (((item.get("organizer") or {}).get("emailAddress")) or {}).get("name")
                or "Unknown"
            ),
            "mustAttend": item.get("responseStatus", {}).get("response", "none")
            != "declined",
            "prepNote": "Review agenda, open related mails, and join on time.",
        }
        for item in graph_data.get("calendar", [])
    ]

    tasks = [
        {
            "id": item["id"],
            "title": item.get("title") or "Untitled task",
            "dueAt": ((item.get("dueDateTime") or {}).get("dateTime"))
            or item.get("lastModifiedDateTime"),
            "source": item.get("listName", "To Do"),
            "status": "done" if item.get("status") == "completed" else "pending",
            "percentComplete": 100 if item.get("status") == "completed" else 25,
            "priority": "high" if item.get("importance") == "high" else "medium",
        }
        for item in graph_data.get("tasks", [])
    ]

    reminders = [
        {
            "id": f"task-reminder-{item['id']}",
            "title": f"Task reminder: {item.get('title') or 'Untitled task'}",
            "at": (item.get("reminderDateTime") or {}).get("dateTime")
            or (item.get("dueDateTime") or {}).get("dateTime")
            or item.get("lastModifiedDateTime"),
            "type": "task",
        }
        for item in graph_data.get("tasks", [])
        if (item.get("reminderDateTime") or {}).get("dateTime")
        or (item.get("dueDateTime") or {}).get("dateTime")
    ]

    reminders.extend(
        {
            "id": f"meeting-reminder-{meeting['id']}",
            "title": f"Upcoming meeting: {meeting['title']}",
            "at": meeting["start"],
            "type": "meeting",
        }
        for meeting in meetings[:3]
    )

    return {
        "employee": {
            "name": employee.get("displayName") or employee.get("userPrincipalName"),
            "role": employee.get("jobTitle") or "Employee",
            "timezone": "UTC",
        },
        "integrations": {
            "mode": "graph-live",
            "sourceSummary": (
                "Live Microsoft Graph data from Outlook Mail, Outlook Calendar, "
                "Teams chats, and Microsoft To Do."
            ),
        },
        "messages": messages,
        "meetings": meetings,
        "tasks": tasks,
        "reminders": reminders,
    }


def build_dashboard_view(snapshot: dict) -> dict:
    pending_tasks = [task for task in snapshot["tasks"] if task["status"] != "done"]
    meetings_today = sorted(snapshot["meetings"], key=lambda item: _to_datetime(item["start"]))
    reminders = sorted(snapshot["reminders"], key=lambda item: _to_datetime(item["at"]))
    attention_signals = [
        message
        for message in snapshot["messages"]
        if message["needsReply"] or message["importance"] in {"high", "medium"}
    ]

    priority_queue = [
        {
            "id": task["id"],
            "kind": "task",
            "title": task["title"],
            "when": task["dueAt"],
            "urgency": task["priority"],
            "detail": f"Due {_format_datetime(task['dueAt'])} via {task['source']}",
        }
        for task in pending_tasks
    ]

    priority_queue.extend(
        {
            "id": meeting["id"],
            "kind": "meeting",
            "title": meeting["title"],
            "when": meeting["start"],
            "urgency": "high",
            "detail": (
                f"Starts {_format_datetime(meeting['start'])} "
                f"at {meeting['location']}"
            ),
        }
        for meeting in meetings_today
        if meeting["mustAttend"]
    )

    priority_queue = sorted(priority_queue, key=lambda item: _to_datetime(item["when"]))[:6]

    focus = [
        (
            f"Attend {sum(1 for meeting in meetings_today if meeting['mustAttend'])} "
            "required meetings today."
        ),
        (
            f"Close {sum(1 for task in pending_tasks if task['priority'] == 'high')} "
            "high-priority task items first."
        ),
        (
            f"Reply to {sum(1 for item in attention_signals if item['needsReply'])} "
            "conversations requiring action."
        ),
    ]

    return {
        "headline": f"{snapshot['employee']['name']}'s execution dashboard",
        "subheadline": (
            "Track messages from Teams and Outlook, stay ahead of meetings, "
            "and keep the employee workday organized in one assistant view."
        ),
        "pendingCount": len(pending_tasks),
        "meetingCount": len(meetings_today),
        "alertCount": len(attention_signals) + len(reminders),
        "focus": focus,
        "priorityQueue": priority_queue,
        "meetingsToday": [
            {
                **meeting,
                "displayTime": (
                    f"{_format_time(meeting['start'])} to "
                    f"{_format_time(meeting['end'])} | {meeting['location']}"
                ),
            }
            for meeting in meetings_today
        ],
        "reminders": [
            {
                **reminder,
                "displayAt": _format_datetime(reminder["at"]),
            }
            for reminder in reminders
        ],
        "attentionSignals": [
            {
                **signal,
                "displayReceivedAt": _format_datetime(signal["receivedAt"]),
            }
            for signal in attention_signals
        ],
        "workdayList": [
            {
                **task,
                "displayDueAt": _format_datetime(task["dueAt"]),
            }
            for task in pending_tasks
        ],
        "integrationMode": snapshot["integrations"]["mode"],
        "integrationCopy": snapshot["integrations"]["sourceSummary"],
    }
