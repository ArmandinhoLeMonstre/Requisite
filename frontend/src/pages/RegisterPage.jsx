import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const RegisterPage = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  async function handleRegister() {
    const res = await fetch("http://localhost:8080/api/users", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ name, email, role, password }),
    });

    const data = await res.json();

    if (res.status === 201) {
      navigate("/login");
    }
  }

  function handleLoginNav() {
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-950 py-20 px-5 flex flex-col rounded-2xl gap-3 w-80 shadow-md border border-gray-500">
        <div className="flex flex-col">
          <label className="text-white text-sm">Name</label>
          <input
            autoFocus
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-white text-sm">Email</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-white text-sm">Role</label>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-white text-sm">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm"
          />
        </div>
        <button
          onClick={handleRegister}
          className="bg-gray-600 hover:bg-gray-500 text-white rounded-lg py-2 text-sm"
        >
          Submit
        </button>
        <div className="flex justify-end">
          <button
            onClick={handleLoginNav}
            className="text-gray-500 underline hover:text-gray-400 underline text-sm px-2"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};
