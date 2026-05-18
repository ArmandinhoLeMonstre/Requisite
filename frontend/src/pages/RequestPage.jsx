import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createGroup, getGroupTickets } from "../api/client";

const filterClass = (filter, value) =>
  `py-1 px-3 rounded-md hover:border hover:text-white hover:border-white ${filter === value ? "border border-white text-gray-100" : "text-gray-400"}`;

const groupClass = (code, activeGroup) =>
  `py-1 px-3 rounded-md hover:border hover:text-white hover:border-white ${code === activeGroup ? "border border-white text-gray-200" : "text-gray-400"}`;

const statusClass = (status) => {
  if (status === "pending") {
    return "text-sm text-amber-800 bg-amber-200 border border-amber-200 px-2 rounded-2xl";
  } else if (status === "approved") {
    return "text-sm text-green-800 bg-green-200 border green-amber-200 px-2 rounded-2xl";
  } else {
    return "text-sm text-red-900 bg-red-200 border border-red-200 px-2 rounded-2xl";
  }
};

export const ManagerPage = () => {
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
      const res = await createGroup()
      console.log(res)
      setTickets( await getGroupTickets())
    } catch(error) {
      console.error("Failed to create a group: ", error)
    }
  }

  useEffect(() => {
    refreshGroups();
  }, []);

  if (!tickets || !activeGroup) return <p>Loading...</p>;

  const filtered = tickets.chats[activeGroup].filter(
    (ticket) => filter === "all" || ticket.status === filter,
  );
  return (
    <div className="flex flex-col h-screen border max-w-3xl w-full mx-auto overflow-hidden">
      <div className="flex flex-row justify-start pl-4 gap-3 mt-5 overflow-x-auto">
        {Object.keys(tickets.chats).map((code) => (
          <button
            key={code}
            onClick={() => setActiveGroup(code, activeGroup)}
            className={groupClass(code, activeGroup)}
          >
            {code}
          </button>
        ))}
        { (Object.keys(tickets.chats).length < 8) ? (

        <button onClick={() => newGroup()} className=" text-gray-100 border border-white rounded-md items-cen px-2 hover:text-white">
          + New group
        </button>
        ) : (
          <p></p>
        )}
      </div>
      <div className="flex flex-row gap-3 pt-4 pl-4 text-white">
        <button
          onClick={() => setFilter("all")}
          className={filterClass(filter, "all")}
        >
          All
        </button>
        <button
          onClick={() => setFilter("pending")}
          className={filterClass(filter, "pending")}
        >
          Pending
        </button>
        <button
          onClick={() => setFilter("approved")}
          className={filterClass(filter, "approved")}
        >
          Approved
        </button>
        <button
          onClick={() => setFilter("rejected")}
          className={filterClass(filter, "rejected")}
        >
          Rejected
        </button>
      </div>
      <div className="flex-1 overflow-x-auto">
        <div className="grid grid-cols-2 gap-4 p-4 overflow-y-auto items-start">
          {filtered.map((ticket) => (
            <div
              key={ticket.id}
              onClick={() => navigate(`/requests/${ticket.id}`)}
              className="text-white border border-gray-300 rounded-md p-3 cursor-pointer hover:border-white"
            >
              <div className="flex items-center justify-between mb-2">
                <p className="font-medium">{ticket.user_name}</p>
                <p className={statusClass(ticket.status)}>
                  {ticket.status.charAt(0).toUpperCase() +
                    ticket.status.slice(1)}
                </p>
              </div>
              <p className="text-sm text-gray-300 mb-2">{ticket.description}</p>
              <p className="text-xs text-gray-500">
                {new Date(ticket.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
