import { Navigate } from "react-router-dom"

export const ProtectedRoute = ({ children, requiredRole }) => {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  if (!token) return <Navigate to="/login" />
  if (requiredRole && role !== requiredRole) {
    if (role === "manager") return <Navigate to="/requests" />
    return <Navigate to="/new" />
  }

  return children
}