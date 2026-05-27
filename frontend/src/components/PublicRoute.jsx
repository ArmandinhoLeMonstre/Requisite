import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export const PublicRoute = () => {
  const { user } = useAuth();
  const token = localStorage.getItem("token");

  if (!token) return <Outlet />;
  if (!user) return null;
  if (user.role === "manager") return <Navigate to="/requests" />;
  return <Navigate to="/new" />;
}
