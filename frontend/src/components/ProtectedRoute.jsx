import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import { getMe } from "../api/client";

export const ProtectedRoute = ({ children }) => {
  const [isValid, setIsValid] = useState(null);

  useEffect(() => {
    async function checkToken() {
      const token = localStorage.getItem("token");

      if (!token) {
        setIsValid(false);
        return;
      }

      try {
        await getMe();
        setIsValid(true);
      } catch (error) {
        if (error.status === 401) {
          localStorage.removeItem("token");
          setIsValid(false);
        }
      }
    }

    checkToken();
  }, []);

  if (isValid === null) return <p>Loading...</p>;
  if (!isValid) return <Navigate to="/login" />;
  return children;
};
