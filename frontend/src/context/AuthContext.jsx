import { createContext, useContext, useEffect, useState } from "react";
import { getMe } from "../api/client";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  }

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;
    async function fetchUser() {
      try {
        const res = await getMe();
        setUser(res.data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
