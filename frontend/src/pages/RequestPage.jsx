import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createGroup, getGroupTickets } from "../api/client";

const filterClass = (filter, value) =>
  `py-1 px-4 rounded-full text-sm transition-colors ${filter === value ? "bg-gray-700 text-white border border-gray-500" : "text-gray-400 hover:text-white"}`;

const groupClass = (code, activeGroup) =>
  `py-1 px-4 rounded-full text-sm font-medium transition-colors ${code === activeGroup ? "bg-gray-700 text-white border border-gray-500" : "text-gray-400 hover:text-white border border-transparent"}`;

const statusClass = (status) => {
  if (status === "pending")
    return "text-xs text-amber-800 bg-amber-200 border border-amber-300 px-2.5 py-0.5 rounded-full font-medium";
  if (status === "approved")
    return "text-xs text-green-800 bg-green-200 border border-green-300 px-2.5 py-0.5 rounded-full font-medium";
  return "text-xs text-red-900 bg-red-200 border border-red-300 px-2.5 py-0.5 rounded-full font-medium";
};

export const RequestPage = () => {
  const [tickets, setTickets] = useState(null);
  const [activeGroup, setActiveGroup] = useState(null);
  const [filter, setFilter] = useState("all");
  const navigate = useNavigate();

  async function refreshGroups() {
    try {
      const tickets_list = await getGroupTickets();
      const keys = Object.keys(tickets_list.chats);
      setTickets(tickets_list);
      setActiveGroup(keys[0]);
    } catch (error) {
      console.error("Failed to load tickets: ", error);
    }
  }

  async function newGroup() {
    try {
      const res = await createGroup();
      const updated = await getGroupTickets();
      const keys = Object.keys(updated.chats);
      setTickets(updated);
      if (!keys.includes(activeGroup)) setActiveGroup(keys[0]);
    } catch (error) {
      console.error("Failed to create a group: ", error);
    }
  }

  useEffect(() => {
    refreshGroups();
  }, []);

  if (!tickets || !activeGroup)
    return <p className="text-gray-400 p-8">Loading...</p>;

  const filtered = tickets.chats[activeGroup].filter(
    (ticket) => filter === "all" || ticket.status === filter,
  );

  return (
    <div className="flex flex-col h-screen max-w-3xl w-full mx-auto overflow-hidden">
      <div className="px-6 pt-6 pb-4 border-b border-gray-800">
        <div className="flex items-center gap-2 mb-5 overflow-x-auto">
          {Object.keys(tickets.chats).map((code) => (
            <button
              key={code}
              onClick={() => setActiveGroup(code)}
              className={groupClass(code, activeGroup)}
            >
              {code}
            </button>
          ))}
          {Object.keys(tickets.chats).length < 4 && (
            <button
              onClick={newGroup}
              className="py-1 px-4 rounded-full text-sm text-gray-400 border border-dashed border-gray-600 hover:text-white hover:border-gray-400 transition-colors"
            >
              + New group
            </button>
          )}
        </div>

        <div className="flex gap-2">
          {["all", "pending", "approved", "rejected"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={filterClass(filter, f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>
      <div className="px-6 pt-4">
        <p className="text-gray-500 text-xs uppercase tracking-widest mb-1">
          Group
        </p>
        <p className="text-white text-xl font-medium">{activeGroup}</p>
      </div>
      <div className="flex-1 overflow-y-auto px-6 py-5">
        {filtered.length === 0 ? (
          <div className="flex justify-center items-center h-40">
            <p className="text-gray-500 text-sm">No tickets found</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4 items-start">
            {filtered.map((ticket) => (
              <div
                key={ticket.id}
                onClick={() =>
                  navigate(`/requests/${ticket.id}`, { state: { ticket } })
                }
                className="flex flex-col gap-2 bg-gray-900 border border-gray-700 rounded-lg p-4 cursor-pointer hover:border-gray-500 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <p className="text-white font-medium text-sm">
                    {ticket.user_name}
                  </p>
                  <span className={statusClass(ticket.status)}>
                    {ticket.status.charAt(0).toUpperCase() +
                      ticket.status.slice(1)}
                  </span>
                </div>
                <p className="text-gray-400 text-sm leading-snug">
                  {ticket.description}
                </p>
                <p className="text-gray-600 text-xs">
                  {new Date(ticket.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
