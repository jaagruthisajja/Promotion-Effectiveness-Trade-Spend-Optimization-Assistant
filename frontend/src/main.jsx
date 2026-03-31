import React from "react";
import ReactDOM from "react-dom/client";
import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";
import App from "./App";
import "./styles.css";
import { isMsalConfigured, msalConfig } from "./authConfig";

const app = (
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

const root = ReactDOM.createRoot(document.getElementById("root"));

if (isMsalConfigured()) {
  const msalInstance = new PublicClientApplication(msalConfig);

  root.render(<MsalProvider instance={msalInstance}>{app}</MsalProvider>);
} else {
  root.render(app);
}
