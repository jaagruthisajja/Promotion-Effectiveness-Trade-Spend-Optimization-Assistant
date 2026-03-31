from datetime import datetime


def _to_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _format_datetime(value: str) -> str:
    return _to_datetime(value).strftime("%d %b %Y, %I:%M %p")


def _format_time(value: str) -> str:
    return _to_datetime(value).strftime("%I:%M %p")


def build_dashboard_view(snapshot: dict) -> dict:
    pending_tasks = [task for task in snapshot["tasks"] if task["status"] != "done"]
    meetings_today = sorted(snapshot["meetings"], key=lambda item: _to_datetime(item["start"]))
    reminders = sorted(snapshot["reminders"], key=lambda item: _to_datetime(item["at"]))
    attention_signals = [
        message
        for message in snapshot["messages"]
        if message["needsReply"] or message["importance"] == "high"
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
