import { useState, useEffect } from "react";
import { getGroup, joinGroup } from "../api/client";
import { useAuth } from "../context/AuthContext";

export const MePage = () => {
  const { user, setUser } = useAuth();
  const [group, setGroup] = useState(null);
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);

  async function submitCode() {
    try {
      const response = await joinGroup(user.id, code);
      const data = response.data;
      if (data.group_id) {
        const group = await getGroup(data.group_id);
        setGroup(group.data);
        setUser({ ...user, group_id: data.group_id });
      }
    } catch (error) {
      if (error.status === 404) {
        setErrorMessage("Invalid Code");
      }
    }
  }

  useEffect(() => {
    async function loadUser() {
      try {
        if (user?.group_id) {
          const group = await getGroup(user.group_id);
          setGroup(group.data);
        }
      } catch (error) {
        console.error(error);
      }
    }
    loadUser();
  }, [user?.group_id]);

  if (!user)
    return (
      <div className="flex flex-col h-screen w-screen items-center justify-center bg-gray-950">
        <div className="text-xl pb-3 text-white">Loading...</div>
        <div className="w-6 h-6 rounded-full border-2 border-gray-600 border-t-white animate-spin" />
      </div>
    );

  return (
    <div className="flex-1 flex items-center justify-center pb-10">
      <div className="w-full max-w-md flex flex-col gap-1">
        <div className="flex items-center gap-3 px-2 pb-4">
          <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-white text-sm font-medium">
            {user.name.slice(0, 2).toUpperCase()}
          </div>
          <div>
            <p className="text-white font-medium text-sm">{user.name}</p>
            <p className="text-gray-500 text-xs">{user.email}</p>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
          <div className="flex justify-between items-center px-4 py-3 border-b border-gray-700">
            <span className="text-gray-500 text-sm">Name</span>
            <span className="text-white text-sm">{user.name}</span>
          </div>
          <div className="flex justify-between items-center px-4 py-3 border-b border-gray-700">
            <span className="text-gray-500 text-sm">Email</span>
            <span className="text-white text-sm">{user.email}</span>
          </div>
          <div className="flex justify-between items-center px-4 py-3 border-b border-gray-700">
            <span className="text-gray-500 text-sm">Role</span>
            <span className="text-white text-sm capitalize">{user.role}</span>
          </div>
          <div className="flex justify-between items-center px-4 py-3">
            <span className="text-gray-500 text-sm">Group</span>
            {user.group_id ? (
              <span className="text-white text-sm font-mono tracking-widest">
                {group?.code}
              </span>
            ) : (
              <div className="flex flex-col items-end gap-1">
                <div className="flex gap-2">
                  <input
                    type="text"
                    className="bg-gray-800 border border-gray-600 text-white text-sm rounded-lg px-3 py-1 w-28 tracking-widest placeholder-gray-600 outline-none focus:border-gray-400"
                    maxLength={5}
                    value={code}
                    onChange={(e) => setCode(e.target.value.toUpperCase())}
                    placeholder="4F3DY"
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && code.trim()) submitCode();
                    }}
                  />
                  <button
                    onClick={() => {
                      if (code) submitCode();
                    }}
                    className="bg-green-700 hover:bg-green-600 text-white text-sm rounded-lg px-3 py-1 transition-colors"
                  >
                    Join
                  </button>
                </div>
                {errorMessage && (
                  <p className="text-red-400 text-xs">{errorMessage}</p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
