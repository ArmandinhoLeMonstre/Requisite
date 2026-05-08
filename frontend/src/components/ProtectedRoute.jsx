import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";

export const ProtectedRoute = ({ children }) => {
  const [isValid, setIsValid] = useState(null);

  useEffect(() => {
    async function checkToken() {
      const token = localStorage.getItem("token");

      if (!token) {
        setIsValid(false);
        return;
      }

      const res = await fetch("http://localhost:8080/api/users/me", {
        headers: { "Authorization": `Bearer ${token}` },
      });

      if (res.status === 401) {
        localStorage.removeItem("token"); // clean up the expired token
        setIsValid(false);
        return;
      }

      setIsValid(true);
    }

    checkToken();
  }, []);

  if (isValid === null) return <p>Loading...</p>;
  if (!isValid) return <Navigate to="/login" />;
  return children;
};