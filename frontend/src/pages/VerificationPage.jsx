import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { verifyUser } from "../api/client";

export const VerificationPage = () => {
  const { token } = useParams();
  const [status, setStatus] = useState("loading");
  const navigate = useNavigate();

  useEffect(() => {
    async function verify(token) {
      try {
        const res = await verifyUser(token);
        setStatus("success");
        setTimeout(() => navigate("/login"), 3000);
      } catch {
        setStatus("error");
      }
    }
    verify(token);
  }, [token]);

  return (
    <div className="flex h-screen justify-center items-center bg-gray-950">
      {status === "loading" && (
        <div className="w-6 h-6 rounded-full border-2 border-gray-600 border-t-white animate-spin" />
      )}
      {status === "success" && (
        <div className="flex flex-col items-center gap-2">
          <p className="text-white font-medium">Email verified</p>
          <p className="text-gray-400 text-sm">
            Redirecting to login in 3 seconds...
          </p>
        </div>
      )}
      {status === "error" && (
        <div className="flex flex-col items-center gap-2">
          <p className="text-white font-medium">Invalid or expired link</p>
          <p className="text-gray-400 text-sm">
            Please request a new verification email.
          </p>
        </div>
      )}
    </div>
  );
};
