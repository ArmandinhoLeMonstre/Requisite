import { useNavigate } from "react-router-dom";

function Sidebar({ tickets }) {
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
        <button
          onClick={handleLogout}
          className="bg-gray-600 hover:bg-gray-500 text-white rounded-lg py-2 text-sm w-full"
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Sidebar;
