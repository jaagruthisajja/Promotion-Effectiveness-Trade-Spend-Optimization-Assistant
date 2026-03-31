import { mockEmployeeSnapshot } from "../data/mock-data.js";

const graphModeDescription =
  "Connect Microsoft Graph to replace mock data with Teams chats, Outlook mail, calendar events, and To Do tasks.";

export async function loadAssistantData() {
  const params = new URLSearchParams(window.location.search);
  const mode = params.get("mode") || "mock";

  if (mode === "graph") {
    return {
      ...mockEmployeeSnapshot,
      integrations: {
        mode: "graph-placeholder",
        sourceSummary: graphModeDescription,
      },
    };
  }

  return mockEmployeeSnapshot;
}
