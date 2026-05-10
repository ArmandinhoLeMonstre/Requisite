import { Routes, Route, Navigate } from "react-router-dom";
import { LoginPage } from "./pages/LoginPage";
import { MePage } from "./pages/MePage";
import { RegisterPage } from "./pages/RegisterPage";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { ChatLayout } from "./components/ChatLayout";
import { TicketPage } from "./pages/TicketPage";
import { NewTicketPage } from "./pages/NewTicketPage";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        element={
          <ProtectedRoute>
            <ChatLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/new" element={<NewTicketPage />} />
        <Route path="/ticket/:ticketId" element={<TicketPage />} />
        <Route path="/me" element={<MePage />} />
        <Route path="/" element={<Navigate to="/new" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
