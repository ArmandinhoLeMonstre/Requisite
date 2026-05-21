import { Navigate, Outlet } from "react-router-dom";

export const PublicRoute = () => {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  if (!token) return <Outlet />
  if (role === "manager") return <Navigate to="/requests" />
  return <Navigate to="/new" />
}
