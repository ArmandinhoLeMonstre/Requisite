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
      setUser(user.data);
      user.data.role === "employee" ? navigate("/new") : navigate("/requests");
    } catch (error) {
      if (error.status === 401) {
        setLoginError(error.response.data.detail);
      }
      console.error(error);
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center gap-10">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-green-600 flex items-center justify-center text-xl font-bold text-white">
          R
        </div>
        <h1 className="text-white text-2xl font-medium tracking-tight">
          Requisite
        </h1>
      </div>

      <div className="w-full max-w-sm flex flex-col gap-5">
        <div className="text-center">
          <h2 className="text-white text-xl font-medium">Sign in</h2>
          <p className="text-gray-500 text-sm mt-1">
            Enter your credentials to continue
          </p>
        </div>

        {loginError && (
          <p className="text-red-400 text-sm text-center bg-red-950 border border-red-800 rounded-lg px-4 py-2">
            {loginError}
          </p>
        )}

        <div className="flex flex-col gap-3">
          <div className="flex flex-col gap-1.5">
            <label className="text-gray-400 text-xs">Email</label>
            <input
              autoFocus
              placeholder="email@example.com"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loginLock) handleLogin();
              }}
              className="bg-gray-900 border border-gray-700 focus:border-gray-500 text-white placeholder-gray-600 rounded-lg px-3 py-2.5 text-sm outline-none transition-colors"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-gray-400 text-xs">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loginLock) handleLogin();
              }}
              className="bg-gray-900 border border-gray-700 focus:border-gray-500 text-white placeholder-gray-600 rounded-lg px-3 py-2.5 text-sm outline-none transition-colors"
            />
          </div>
        </div>

        <button
          disabled={loginLock}
          onClick={handleLogin}
          className="w-full bg-green-700 hover:bg-green-600 disabled:bg-gray-800 disabled:text-gray-600 disabled:cursor-not-allowed text-white rounded-lg py-2.5 text-sm font-medium transition-colors"
        >
          Sign in
        </button>

        <p className="text-center text-sm text-gray-500">
          Don't have an account?{" "}
          <button
            onClick={() => navigate("/register")}
            className="text-gray-300 hover:text-white transition-colors"
          >
            Register
          </button>
        </p>
      </div>
    </div>
  );
};
