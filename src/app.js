import { loadAssistantData } from "./services/data-service.js";
import {
  buildDashboardView,
  formatDateTime,
  formatTime,
} from "./services/assistant-engine.js";

const elements = {
  integrationBadge: document.querySelector("#integration-badge"),
  integrationCopy: document.querySelector("#integration-copy"),
  assistantFocus: document.querySelector("#assistant-focus"),
  headline: document.querySelector("#headline"),
  subheadline: document.querySelector("#subheadline"),
  pendingCount: document.querySelector("#pending-count"),
  meetingCount: document.querySelector("#meeting-count"),
  alertCount: document.querySelector("#alert-count"),
  priorityQueue: document.querySelector("#priority-queue"),
  meetingList: document.querySelector("#meeting-list"),
  reminderList: document.querySelector("#reminder-list"),
  signalList: document.querySelector("#signal-list"),
  workdayList: document.querySelector("#workday-list"),
  refreshButton: document.querySelector("#refresh-button"),
};

function renderListItem({
  kicker,
  title,
  meta,
  chips = [],
  emphasize = false,
}) {
  const item = document.createElement("article");
  item.className = "list-item";

  item.innerHTML = `
    <div class="list-item-header">
      <span class="item-kicker">${kicker}</span>
      <span class="muted">${emphasize ? "Action now" : ""}</span>
    </div>
    <h4>${title}</h4>
    <p class="list-meta">${meta}</p>
    <div class="chip-row">
      ${chips
        .map(
          (chip) =>
            `<span class="chip ${chip.tone}">${chip.label}</span>`,
        )
        .join("")}
    </div>
  `;

  return item;
}

function renderWorkdayItem(task) {
  const item = document.createElement("article");
  item.className = "workday-item";
  item.innerHTML = `
    <div class="workday-header">
      <div>
        <p class="item-kicker">${task.source}</p>
        <h4>${task.title}</h4>
      </div>
      <strong>${task.percentComplete}%</strong>
    </div>
    <p class="list-meta">Due ${formatDateTime(task.dueAt)} | Priority ${task.priority}</p>
    <div class="progress">
      <span style="width: ${task.percentComplete}%"></span>
    </div>
  `;
  return item;
}

function clearChildren(node) {
  node.replaceChildren();
}

function renderDashboard(view) {
  elements.integrationBadge.textContent =
    view.integrationMode === "mock" ? "Mock Data" : "Graph Ready";
  elements.integrationCopy.textContent = view.integrationCopy;
  elements.headline.textContent = view.headline;
  elements.subheadline.textContent = view.subheadline;
  elements.pendingCount.textContent = String(view.pendingCount);
  elements.meetingCount.textContent = String(view.meetingCount);
  elements.alertCount.textContent = String(view.alertCount);

  clearChildren(elements.assistantFocus);
  view.focus.forEach((line) => {
    const item = document.createElement("li");
    item.textContent = line;
    elements.assistantFocus.appendChild(item);
  });

  clearChildren(elements.priorityQueue);
  view.priorityQueue.forEach((item) => {
    elements.priorityQueue.appendChild(
      renderListItem({
        kicker: item.kind,
        title: item.title,
        meta: item.detail,
        emphasize: item.urgency === "high",
        chips: [
          {
            label: item.urgency,
            tone: item.urgency === "high" ? "chip-warn" : "chip-accent",
          },
        ],
      }),
    );
  });

  clearChildren(elements.meetingList);
  view.meetingsToday.forEach((meeting) => {
    elements.meetingList.appendChild(
      renderListItem({
        kicker: meeting.mustAttend ? "Required" : "Optional",
        title: meeting.title,
        meta: `${formatTime(meeting.start)} to ${formatTime(meeting.end)} | ${meeting.location}`,
        chips: [
          {
            label: meeting.organizer,
            tone: "chip-info",
          },
          {
            label: meeting.prepNote,
            tone: "chip-accent",
          },
        ],
      }),
    );
  });

  clearChildren(elements.reminderList);
  view.reminders.forEach((reminder) => {
    elements.reminderList.appendChild(
      renderListItem({
        kicker: reminder.type,
        title: reminder.title,
        meta: formatDateTime(reminder.at),
        chips: [
          {
            label: "Reminder",
            tone: reminder.type === "meeting" ? "chip-info" : "chip-warn",
          },
        ],
      }),
    );
  });

  clearChildren(elements.signalList);
  view.attentionSignals.forEach((signal) => {
    elements.signalList.appendChild(
      renderListItem({
        kicker: signal.source,
        title: signal.subject,
        meta: `${signal.sender} | ${formatDateTime(signal.receivedAt)}`,
        chips: [
          {
            label: signal.importance,
            tone: signal.importance === "high" ? "chip-warn" : "chip-accent",
          },
          {
            label: signal.needsReply ? "Reply needed" : "FYI",
            tone: "chip-info",
          },
          {
            label: signal.extractedTask,
            tone: "chip-accent",
          },
        ],
      }),
    );
  });

  clearChildren(elements.workdayList);
  view.workdayList.forEach((task) => {
    elements.workdayList.appendChild(renderWorkdayItem(task));
  });
}

async function bootstrap() {
  const snapshot = await loadAssistantData();
  const view = buildDashboardView(snapshot);
  renderDashboard(view);
}

elements.refreshButton.addEventListener("click", bootstrap);

bootstrap();
