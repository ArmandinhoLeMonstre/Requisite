import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createToken, getMe } from "../api/client";
import { useAuth } from "../context/AuthContext";

export const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState(false);
  const loginLock = email.trim() === "" || password.trim() === "";
  const { setUser } = useAuth();
  const navigate = useNavigate();

  async function handleLogin() {
    try {
      const res = await createToken(email, password);
      localStorage.setItem("token", res.access_token);
      const user = await getMe();
      localStorage.setItem("role", user.data.role);
      setUser(user.data);
      user.data.role === "employee" ? navigate("/new") : navigate("/requests");
    } catch (error) {
      if (error.status === 401) {
        setLoginError(error.response.data.detail);
      }
      console.error(error);
      return;
    }
  }

  function handleRegisterNav() {
    navigate("/register");
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center ">
      <div className="flex-col-reverse  border border-white mb-40">
        <h1 className="text-white text-6xl">REQUISITE</h1>
      </div>
      <div className="bg-gray-950 pb-18 pt-10 px-5 flex flex-col rounded-2xl gap-3 w-80 shadow-md border border-gray-500">
        <div>
          <h1 className="text-white text-center text-3xl pb-8">Sign in</h1>
        </div>
        {loginError && (
          <div>
            <p className="text-red-500 text-center text-sm">{loginError}</p>
          </div>
        )}
        <div className="flex flex-col text-white">
          <label className=" text-sm">Email</label>
          <input
            onKeyDown={(e) => {
              if (e.key === "Enter" && !loginLock) {
                handleLogin();
              }
            }}
            autoFocus
            placeholder="email@example.com"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />
        </div>
        <div className="flex flex-col text-white">
          <label className="text-sm">Password</label>
          <input
            onKeyDown={(e) => {
              if (e.key === "Enter" && !loginLock) {
                handleLogin();
              }
            }}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />
        </div>
        <div className="flex min-w-full">
          <button
            disabled={loginLock}
            onClick={handleLogin}
            className="bg-gray-600 hover:bg-gray-500 text-white rounded-lg py-2 text-sm w-full disabled:bg-gray-950 disabled:border disabled:border-gray-500"
          >
            Submit
          </button>
        </div>
        <div className="flex justify-end">
          <button
            onClick={handleRegisterNav}
            className="text-gray-500 underline hover:text-gray-400 text-sm px-2"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};
