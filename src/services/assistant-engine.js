function toDate(value) {
  return new Date(value);
}

function sortByDateAscending(items, key) {
  return [...items].sort((a, b) => toDate(a[key]) - toDate(b[key]));
}

export function buildDashboardView(snapshot) {
  const pendingTasks = snapshot.tasks.filter((task) => task.status !== "done");
  const meetingsToday = sortByDateAscending(snapshot.meetings, "start");
  const reminders = sortByDateAscending(snapshot.reminders, "at");
  const attentionSignals = snapshot.messages.filter(
    (message) => message.needsReply || message.importance === "high",
  );

  const priorityQueue = [
    ...pendingTasks.map((task) => ({
      id: task.id,
      kind: "task",
      title: task.title,
      when: task.dueAt,
      urgency: task.priority,
      detail: `Due ${formatDateTime(task.dueAt)} via ${task.source}`,
    })),
    ...meetingsToday
      .filter((meeting) => meeting.mustAttend)
      .map((meeting) => ({
        id: meeting.id,
        kind: "meeting",
        title: meeting.title,
        when: meeting.start,
        urgency: "high",
        detail: `Starts ${formatDateTime(meeting.start)} at ${meeting.location}`,
      })),
  ]
    .sort((a, b) => toDate(a.when) - toDate(b.when))
    .slice(0, 6);

  const focus = [
    `Attend ${meetingsToday.filter((meeting) => meeting.mustAttend).length} required meetings today.`,
    `Close ${pendingTasks.filter((task) => task.priority === "high").length} high-priority task items first.`,
    `Reply to ${attentionSignals.filter((signal) => signal.needsReply).length} conversations requiring action.`,
  ];

  return {
    headline: `${snapshot.employee.name}'s execution dashboard`,
    subheadline: `Track messages from Teams and Outlook, stay ahead of meetings, and keep the employee workday organized in one assistant view.`,
    pendingCount: pendingTasks.length,
    meetingCount: meetingsToday.length,
    alertCount: attentionSignals.length + reminders.length,
    focus,
    priorityQueue,
    meetingsToday,
    reminders,
    attentionSignals,
    workdayList: pendingTasks,
    integrationMode: snapshot.integrations.mode,
    integrationCopy: snapshot.integrations.sourceSummary,
  };
}

export function formatDateTime(value) {
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(toDate(value));
}

export function formatTime(value) {
  return new Intl.DateTimeFormat("en-IN", {
    timeStyle: "short",
  }).format(toDate(value));
}
