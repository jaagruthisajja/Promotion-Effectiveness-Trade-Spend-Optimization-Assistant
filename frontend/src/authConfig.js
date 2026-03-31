export const msalConfig = {
  auth: {
    clientId: import.meta.env.VITE_AZURE_CLIENT_ID || "",
    authority: `https://login.microsoftonline.com/${
      import.meta.env.VITE_AZURE_TENANT_ID || "common"
    }`,
    redirectUri:
      import.meta.env.VITE_AZURE_REDIRECT_URI || "http://127.0.0.1:5173",
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false,
  },
};

export const loginRequest = {
  scopes: [
    "User.Read",
    "Mail.Read",
    "Calendars.Read",
    "Tasks.Read",
    "Chat.Read",
  ],
};

export function isMsalConfigured() {
  return Boolean(import.meta.env.VITE_AZURE_CLIENT_ID);
}
