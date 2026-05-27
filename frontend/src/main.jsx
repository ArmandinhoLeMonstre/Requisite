import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { ErrorBoundary } from "react-error-boundary";
import "./index.css";
import App from "./App.jsx";
import ErrorFallback from "./pages/errors/ErrorFallback.jsx";

const toastOptions = {
  style: {
    background: "#1f2937",
    color: "#fff",
    border: "1px solid #374151",
  },
  error: {
    iconTheme: {
      primary: "#ef4444",
      secondary: "#fff",
    },
  },
};

createRoot(document.getElementById("root")).render(
  <ErrorBoundary FallbackComponent={ErrorFallback}>
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={toastOptions} />
      <App />
    </BrowserRouter>
  </ErrorBoundary>,
);
