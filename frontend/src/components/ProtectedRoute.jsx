import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export const ProtectedRoute = ({ children, requiredRole }) => {
  const { user } = useAuth();

  const token = localStorage.getItem("token")
  const role = user?.role

  if (!token) return <Navigate to="/login" />
  if (!user) return (
  <div className="flex h-screen items-center justify-center bg-gray-950">
    <div className="w-6 h-6 rounded-full border-2 border-gray-600 border-t-white animate-spin" />
  </div>
);
  if (requiredRole && role !== requiredRole) {
    if (role === "manager") return <Navigate to="/requests" />
    return <Navigate to="/new" />
  }

  return children
}