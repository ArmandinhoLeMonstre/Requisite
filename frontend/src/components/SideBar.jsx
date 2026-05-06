function Sidebar({ tickets, onTicketClick }) {

  return (
    <div className="w-64 bg-gray-900 flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-lg font-semibold text-white">My Tickets</h1>
      </div>
      <div className="flex-1 overflow-y-auto p-2">
        {tickets.length > 0 ? (
          tickets.map((ticket) => (
            <button
              key={ticket.id}
              onClick={() => onTicketClick(ticket.id)}
              className="w-full text-left text-gray-300 hover:bg-gray-700 rounded px-5 py-2"
            >
              {ticket.title}
            </button>
          ))
        ) : (
          <p className="text-gray-500 text-md p-2">No tickets yet</p>
        )}
      </div>
    </div>
  );
}

export default Sidebar;
