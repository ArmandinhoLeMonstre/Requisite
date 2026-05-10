import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getMe } from "../api/client";

export const MePage = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadUser() {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const res = await getMe();
		const data = await res.data;
        setUser(data);
      } catch (error) {
        if (error.status === 401) {
          localStorage.removeItem("token");
          navigate("/login");
        }
      }

    }
    loadUser();
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div className="flex-1 flex items-center justify-center border border-white">
        <h1 className="text-white text-3xl ">Name: {user.name}</h1>
    </div>
  );
};
