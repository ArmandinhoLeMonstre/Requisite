import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Sidebar({ tickets }) {
	const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <div className="w-64 bg-gray-900 flex flex-col border-r border-r-gray-400">
      <div className="p-4 border-b border-gray-400">
        <h1 className="text-lg font-semibold text-white">My Tickets</h1>
      </div>
      <div className="flex-1 overflow-y-auto p-2">
        {tickets.length > 0 ? (
          tickets.map((ticket) => (
            <button
              key={ticket.id}
              onClick={() => navigate(`/ticket/${ticket.id}`)}
              className="w-full text-sm text-left text-gray-200 hover:bg-gray-700 rounded px-1 py-1"
            >
              {ticket.id}
            </button>
          ))
        ) : (
          <p className="text-gray-500 text-md p-2">No tickets yet</p>
        )}
      </div>
      <div className="mx-3 mb-2">
		{menuOpen && (
			<div className="absolute bottom-12 left-0 bg-white rounded-xl overflow-hidden">
				<button
				onClick={() => navigate("/me")}
				className="w-full px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 text-left"
				>
					Profile
				</button>
				<hr />
				<button
					onClick={handleLogout}
					className="w-full px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 text-left"
				>
					Logout
				</button>
			</div>
		)}
		<div
			onClick={() => setMenuOpen(!menuOpen)}
			className="flex items-center gap-3 cursor-pointer hover:bg-gray-700 rounded-lg p-2"
		>
		  <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-white text-sm font-medium">
		  U
		  </div>
		  <span className="text-white text-sm">User</span>

		</div>
      </div>
    </div>
  );
}

export default Sidebar;
