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
      <div className="bg-white rounded-2xl shadow-sm border w-full max-w-lg p-8 flex flex-col gap-4">
        <h1 className="text-xl font-semibold text-gray-400">My profile</h1>

        <hr />

        <div className="flex justify-between items-center">
          <span className="text-gray-500 text-sm">Name</span>
          <span className="text-gray-900 text-sm">{user.name}</span>
        </div>

        <hr />

        <div className="flex justify-between items-center">
          <span className="text-gray-500 text-sm">Email</span>
          <span className="text-gray-900 text-sm">{user.email}</span>
        </div>

        <hr />

        <div className="flex justify-between items-center">
          <span className="text-gray-500 text-sm">Role</span>
          <span className="text-gray-900 text-sm">{user.role}</span>
        </div>
      </div>
    </div>
  );
};
