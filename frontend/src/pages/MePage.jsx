import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getGroup, getMe, joinGroup } from "../api/client";

export const MePage = () => {
  const [user, setUser] = useState(null);
  const [group, setGroup] = useState(null);
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);
  const navigate = useNavigate();

  async function submitCode() {
    console.log(user.id);
    try {
      const response = await joinGroup(user.id, code);
      const data = response.data;
      if (data.group_id) {
        const group = await getGroup(data.group_id);
        setGroup(group.data);
      }
    } catch (error) {
      if (error.status === 404) {
        setErrorMessage("Invalid Code");
      }
      console.log(error);
    }
  }

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
        if (data.group_id) {
          const group = await getGroup(data.group_id);
          setGroup(group.data);
        }
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
      <div className="bg-white rounded-2xl shadow-sm border w-full max-w-lg p-8 pb-6 flex flex-col gap-4">
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

        <hr />

        <div className="flex justify-between ">
          <span className="text-gray-500 text-sm flex flex-1 ">Group</span>
          {group ? (
            <span className="text-gray-900 text-sm">{group.code}</span>
          ) : (
            <div className="flex flex-col">
              <div className="overflow-hidden flex">
                <input
                  type="text"
                  className="w-17 pl-2 border rounded-2xl mr-2"
                  maxLength={5}
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="4F3DY"
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && code && code.trim() !== "" ) {
                      submitCode();
                    }
                  }}
                />
                <button
                  className=" rounded-4xl p-3 bg-green-500 border"
                  onClick={() => {
                    if (code) {
                      submitCode();
                    }
                  }}
                ></button>
              </div>
              {errorMessage ? (
                <div className=" pl-4">
                  <p className="text-red-700 text-sm">{errorMessage}</p>
                </div>
              ) : (
                <p />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
