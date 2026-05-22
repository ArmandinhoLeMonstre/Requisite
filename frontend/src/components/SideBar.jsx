import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Sidebar({ tickets }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const {user, handleLogout} = useAuth()
  const navigate = useNavigate();

  const initials = user?.name ? user.name.slice(0, 2).toUpperCase() : "U";

  return (
    <div className="w-56 bg-gray-900 flex flex-col border-r border-gray-700">

      <div className="p-4 border-b border-gray-700 flex items-center gap-2">
        <div className="w-6 h-6 rounded-md bg-green-600 flex items-center justify-center text-sm font-bold text-white flex-shrink-0">
          R
        </div>
        <span className="text-white text-sm font-medium">Requisite</span>
      </div>

      <div className="px-3 pt-4 pb-2 flex items-center justify-between">
        <span className="text-xs text-gray-500 uppercase tracking-widest">My Tickets</span>
        <button
          onClick={() => navigate("/new")}
          className="text-xs text-gray-400 hover:text-white border border-gray-600 hover:border-gray-400 rounded-md px-2 py-0.5 transition-colors"
        >
          + New
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 flex flex-col gap-0.5">
        {tickets.length > 0 ? (
          tickets.map((ticket) => (
            <button
              key={ticket.id}
              onClick={() => navigate(`/ticket/${ticket.id}`)}
              className="w-full text-left text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-md px-3 py-2 truncate transition-colors"
            >
              {ticket.description}
            </button>
          ))
        ) : (
          <p className="text-gray-600 text-sm px-3 py-2">No tickets yet</p>
        )}
      </div>

      <div className="relative p-2 border-t border-gray-700">
        {menuOpen && (
          <div className="absolute bottom-full left-2 right-2 mb-1 bg-gray-800 border border-gray-600 rounded-xl overflow-hidden shadow-lg">
            <button
              onClick={() => { navigate("/me"); setMenuOpen(false); }}
              className="w-full px-4 py-3 text-sm text-gray-300 hover:bg-gray-700 hover:text-white text-left transition-colors"
            >
              Profile
            </button>
            <hr className="border-gray-600" />
            <button
              onClick={handleLogout}
              className="w-full px-4 py-3 text-sm text-gray-300 hover:bg-gray-700 hover:text-white text-left transition-colors"
            >
              Logout
            </button>
          </div>
        )}
        <div
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex items-center gap-3 cursor-pointer hover:bg-gray-800 rounded-lg p-2 transition-colors"
        >
          <div className="w-7 h-7 rounded-full bg-gray-600 flex items-center justify-center text-white text-xs font-medium flex-shrink-0">
            {initials}
          </div>
          <span className="text-white text-sm truncate">{user?.name || "User"}</span>
        </div>
      </div>

    </div>
  );
}

export default Sidebar;