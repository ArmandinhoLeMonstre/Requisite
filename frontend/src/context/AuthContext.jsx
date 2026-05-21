import { createContext, useContext, useEffect, useState } from "react";
import { getMe } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

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
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}