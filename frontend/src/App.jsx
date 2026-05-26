import { Routes, Route, Navigate } from "react-router-dom";
import { LoginPage } from "./pages/LoginPage";
import { MePage } from "./pages/MePage";
import { RegisterPage } from "./pages/RegisterPage";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { ChatLayout } from "./components/ChatLayout";
import { TicketPage } from "./pages/TicketPage";
import { NewTicketPage } from "./pages/NewTicketPage";
import { PublicRoute } from "./components/PublicRoute";
import { ManagerLayout } from "./components/ManagerLayout";
import { VerificationPage } from "./pages/VerificationPage";
import { InventoryPage } from "./pages/InventoryPage";
import { RequestPage } from "./pages/RequestPage";
import { ManagerTicketPage } from "./pages/ManagerTicketPage";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route element={<PublicRoute />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/verify/:token" element={<VerificationPage />} />
        </Route>
        <Route
          element={
            <ProtectedRoute requiredRole={"employee"}>
              <ChatLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/new" element={<NewTicketPage />} />
          <Route path="/ticket/:ticketId" element={<TicketPage />} />
          <Route path="/me" element={<MePage />} />
          <Route path="/" element={<Navigate to="/new" replace />} />
        </Route>
        <Route
          element={
            <ProtectedRoute requiredRole={"manager"}>
              <ManagerLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/inventory" element={<InventoryPage />} />
          <Route path="/requests" element={<RequestPage />} />
          <Route path="/requests/:ticketId" element={<ManagerTicketPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
