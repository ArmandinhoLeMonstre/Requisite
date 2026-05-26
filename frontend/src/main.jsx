import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ErrorBoundary } from "react-error-boundary";
import "./index.css";
import App from "./App.jsx";
import ErrorFallback from "./pages/errors/ErrorFallback.jsx";

createRoot(document.getElementById("root")).render(
   <ErrorBoundary FallbackComponent={ErrorFallback}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </ErrorBoundary>,
);
