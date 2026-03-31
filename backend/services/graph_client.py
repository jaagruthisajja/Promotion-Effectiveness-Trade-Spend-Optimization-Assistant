from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx


GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


class GraphAuthError(Exception):
    pass


class GraphApiError(Exception):
    pass


async def _graph_get(
    client: httpx.AsyncClient,
    token: str,
    path: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    response = await client.get(
        f"{GRAPH_BASE_URL}{path}",
        params=params,
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code == 401:
        raise GraphAuthError("Microsoft Graph rejected the access token.")

    if response.status_code >= 400:
        raise GraphApiError(
            f"Graph call failed for {path} with status {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


async def fetch_graph_snapshot(access_token: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    start = now.astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    async with httpx.AsyncClient(timeout=20.0) as client:
        me_task = _graph_get(
            client,
            access_token,
            "/me",
            params={"$select": "displayName,jobTitle,mail,userPrincipalName"},
        )
        messages_task = _graph_get(
            client,
            access_token,
            "/me/messages",
            params={
                "$top": 10,
                "$select": (
                    "id,subject,from,receivedDateTime,importance,isRead,flag"
                ),
                "$orderby": "receivedDateTime desc",
            },
        )
        calendar_task = _graph_get(
            client,
            access_token,
            "/me/calendar/calendarView",
            params={
                "startDateTime": start.isoformat(),
                "endDateTime": end.isoformat(),
                "$top": 10,
                "$select": (
                    "id,subject,start,end,location,organizer,attendees,"
                    "isOrganizer,responseStatus,onlineMeeting,onlineMeetingUrl"
                ),
                "$orderby": "start/dateTime",
            },
        )
        chats_task = _graph_get(
            client,
            access_token,
            "/me/chats",
            params={"$top": 8},
        )
        lists_task = _graph_get(client, access_token, "/me/todo/lists")

        me, messages, calendar, chats, todo_lists = await asyncio.gather(
            me_task,
            messages_task,
            calendar_task,
            chats_task,
            lists_task,
        )

        tasks: list[dict[str, Any]] = []
        for todo_list in todo_lists.get("value", [])[:5]:
            task_payload = await _graph_get(
                client,
                access_token,
                f"/me/todo/lists/{todo_list['id']}/tasks",
                params={
                    "$top": 10,
                    "$select": (
                        "id,title,status,importance,dueDateTime,reminderDateTime,"
                        "body,lastModifiedDateTime"
                    ),
                },
            )

            for item in task_payload.get("value", []):
                item["listName"] = todo_list.get("displayName", "Tasks")
                tasks.append(item)

        chat_signals: list[dict[str, Any]] = []
        for chat in chats.get("value", [])[:4]:
            messages_payload = await _graph_get(
                client,
                access_token,
                f"/chats/{chat['id']}/messages",
                params={"$top": 1},
            )
            latest = (messages_payload.get("value") or [None])[0]
            if latest:
                chat_signals.append(
                    {
                        "id": latest.get("id"),
                        "chatId": chat.get("id"),
                        "topic": chat.get("topic") or "Teams chat",
                        "createdDateTime": latest.get("createdDateTime"),
                        "from": ((latest.get("from") or {}).get("user") or {}).get(
                            "displayName", "Unknown"
                        ),
                        "preview": latest.get("body", {}).get("content", ""),
                    }
                )

    return {
        "me": me,
        "messages": messages.get("value", []),
        "calendar": calendar.get("value", []),
        "tasks": tasks,
        "chatSignals": chat_signals,
    }
