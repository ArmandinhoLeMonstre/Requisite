import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export const ManagerLayout = () => {
  const {user, handleLogout} = useAuth()

  return (
    <div className="h-screen bg-gray-950 overflow-hidden">
      <nav className="flex flex-row fixed top-0 left-0 right-0 z-10 h-14 bg-gray-950 border-b border-gray-800 items-center px-6">
        <div className="flex-1 flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-green-600 flex items-center justify-center text-xs font-bold text-white">
            R
          </div>
          <span className="text-white text-sm font-medium">Requisite</span>
        </div>
        <div className="flex gap-6 text-sm">
          <Link
            to="/requests"
            className="text-white hover:text-gray-300 transition-colors"
          >
            Requests
          </Link>
          <Link
            to="/inventory"
            className="text-white hover:text-gray-300 transition-colors"
          >
            Inventory
          </Link>
        </div>
        <div className="flex-1 flex justify-end items-center gap-3">
          <div className="w-7 h-7 rounded-full bg-slate-800 border border-slate-600 flex items-center justify-center text-xs font-medium text-slate-300">
            {user ? user.name.slice(0, 2).toUpperCase() : ""}
          </div>
          <button
            onClick={handleLogout}
            className="text-sm text-gray-500 hover:text-white transition-colors"
          >
            Logout
          </button>
        </div>
      </nav>
      <main className="pt-16 h-full">
        <Outlet />
      </main>
    </div>
  );
};
