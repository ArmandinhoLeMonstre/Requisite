import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createUser } from "../api/client";

export const RegisterPage = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("employee");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState([]);
  const registerLock =
    name.trim() === "" ||
    email.trim() === "" ||
    password.trim() === "" ||
    role.trim() === "";
  const navigate = useNavigate();

  async function handleRegister() {
    try {
      await createUser(name, email, role, password);
      navigate("/login");
    } catch (error) {
      if (error.status === 400) {
        setErrorMessage([error.response.data.detail]);
      } else if (error.status === 422) {
        setErrorMessage([error.response.data.detail[0].msg]);
      }
      console.error(error);
    }
  }

  const inputClass = "bg-gray-900 border border-gray-700 focus:border-gray-500 text-white placeholder-gray-600 rounded-lg px-3 py-2.5 text-sm outline-none transition-colors";

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center gap-10">

      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-green-600 flex items-center justify-center text-sm font-bold text-white">
          R
        </div>
        <h1 className="text-white text-2xl font-medium tracking-tight">Requisite</h1>
      </div>

      <div className="w-full max-w-sm flex flex-col gap-5">
        <div className="text-center">
          <h2 className="text-white text-xl font-medium">Create an account</h2>
          <p className="text-gray-500 text-sm mt-1">Fill in your details to get started</p>
        </div>

        {errorMessage.length > 0 && (
          <p className="text-red-400 text-sm text-center bg-red-950 border border-red-800 rounded-lg px-4 py-2">
            {errorMessage[0]}
          </p>
        )}

        <div className="flex flex-col gap-3">
          <div className="flex flex-col gap-1.5">
            <label className="text-gray-400 text-xs">Name</label>
            <input
              autoFocus
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !registerLock) handleRegister(); }}
              className={inputClass}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-gray-400 text-xs">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !registerLock) handleRegister(); }}
              className={inputClass}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-gray-400 text-xs">Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className={inputClass}
            >
              <option value="employee">Employee</option>
              <option value="manager">Manager</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-gray-400 text-xs">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !registerLock) handleRegister(); }}
              className={inputClass}
            />
          </div>
        </div>

        <button
          disabled={registerLock}
          onClick={handleRegister}
          className="w-full bg-green-700 hover:bg-green-600 disabled:bg-gray-800 disabled:text-gray-600 disabled:cursor-not-allowed text-white rounded-lg py-2.5 text-sm font-medium transition-colors"
        >
          Create account
        </button>

        <p className="text-center text-sm text-gray-500">
          Already have an account?{" "}
          <button
            onClick={() => navigate("/login")}
            className="text-gray-300 hover:text-white transition-colors"
          >
            Sign in
          </button>
        </p>

      </div>
    </div>
  );
};