import {  useState } from "react";
import { useNavigate } from "react-router-dom";
import { createUser } from "../api/client";

export const RegisterPage = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("employee");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState([]);
  const errorCheck = errorMessage.length === 0;
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

  function handleLoginNav() {
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-950 py-20 px-5 flex flex-col rounded-2xl gap-3 w-80 shadow-md border border-gray-500">
        {errorCheck && (
          <div>
            <p className="text-red-500 text-center text-sm">{errorMessage}</p>
          </div>
        )}
        <div className="flex flex-col">
          <label className="text-white text-sm">Name</label>
          <input
            onKeyDown={(e) => {
              if (e.key === "Enter" && !registerLock) {
                handleRegister();
              }
            }}
            autoFocus
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm text-white"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-white text-sm">Email</label>
          <input
            onKeyDown={(e) => {
              if (e.key === "Enter" && !registerLock) {
                handleRegister();
              }
            }}
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm text-white"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-white text-sm">Role</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="your-existing-input-classes border border-white rounded-lg px-3 py-2 text-sm text-white"
          >
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
          </select>
        </div>
        <div className="flex flex-col">
          <label className="text-white text-sm">Password</label>
          <input
            onKeyDown={(e) => {
              if (e.key === "Enter" && !registerLock) {
                handleRegister();
              }
            }}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border border-white rounded-lg px-3 py-2 text-sm text-white"
          />
        </div>
        <button
          disabled={registerLock}
          onClick={handleRegister}
          className="bg-gray-600 hover:bg-gray-500 text-white rounded-lg py-2 text-sm disabled:bg-gray-950 disabled:border disabled:border-gray-500"
        >
          Submit
        </button>
        <div className="flex justify-end">
          <button
            onClick={handleLoginNav}
            className="text-gray-500 hover:text-gray-400 underline text-sm px-2"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};
