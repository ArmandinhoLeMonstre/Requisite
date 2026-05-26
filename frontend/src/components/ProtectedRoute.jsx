import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export const ProtectedRoute = ({ children, requiredRole }) => {
  const { user } = useAuth();

  const token = localStorage.getItem("token")
  const role = user?.role

  if (!token) return <Navigate to="/login" />
  if (!user) return null;
  if (requiredRole && role !== requiredRole) {
    if (role === "manager") return <Navigate to="/requests" />
    return <Navigate to="/new" />
  }

  return children
}