import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { changeTicketStatus, getChats, getTicket } from "../api/client";
import MessageList from "../components/MessageList";

const statusClass = (status) => {
  if (status === "pending") {
    return "text-sm text-amber-800 bg-amber-200 border border-amber-200 px-2 rounded-2xl";
  } else if (status === "approved") {
    return "text-sm text-green-800 bg-green-200 border border-green-200 px-2 rounded-2xl";
  } else {
    return "text-sm text-red-900 bg-red-200 border border-red-200 px-2 rounded-2xl";
  }
};

export const ManagerTicketPage = () => {
  const location = useLocation();
  const { ticketId } = useParams();
  const [activeTicket, setActiveTicket] = useState(null);
  const [currentTicket, setCurrentTicket] = useState(location.state?.ticket);
  const navigate = useNavigate();

  async function changeStatus(newStatus) {
    try {
      await changeTicketStatus(ticketId, newStatus);
      setCurrentTicket((prev) => ({ ...prev, status: newStatus }));
    } catch (error) {
      console.error("Failed to change the ticket status: ", error);
    }
  }

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getChats(ticketId);
        setActiveTicket(data);
        if (!currentTicket) {
          const ticketData = await getTicket(ticketId);
          setCurrentTicket(ticketData.data);
        }
      } catch (error) {
        console.error("Failed to load the chats: ", error);
      }
    }
    fetchData();
  }, [ticketId]);

  if (!activeTicket || !currentTicket)
  return (
    <div className="flex h-full items-center justify-center">
      <div className="w-6 h-6 rounded-full border-2 border-gray-600 border-t-white animate-spin" />
    </div>
  );
  return (
    <div className="flex flex-col h-full max-w-3xl w-full mx-auto">
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex flex-row items-center text-white p-4 border-b border-gray-700">
            <div className="flex-1 flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-blue-900 border border-blue-700 flex items-center justify-center text-sm font-medium text-blue-200">
                {currentTicket.user_name.slice(0, 2).toUpperCase()}
              </div>
              <div className="flex flex-col gap-1">
                <p className="text-lg font-medium">{currentTicket.user_name}</p>
                <p className="text-sm text-gray-400">
                  {new Date(currentTicket.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
            <p className={statusClass(currentTicket.status)}>
              {currentTicket.status.charAt(0).toUpperCase() +
                currentTicket.status.slice(1)}
            </p>
          </div>
          <div className="flex-shrink-0 mx-4 my-3 p-3 bg-gray-900 rounded-md border border-gray-700">
            <p className="text-xs text-gray-400 mb-1">Request</p>
            <p className="text-sm text-white">{currentTicket.description}</p>
          </div>

          <div className="flex-1 overflow-y-auto">
            <MessageList listMessage={activeTicket.chats} />
          </div>

          <div className="flex items-center justify-between p-4 border-t border-gray-700">
            <button
              className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
              onClick={() => navigate("/requests")}
            >
              ← Back to requests
            </button>

            {currentTicket.status === "pending" ? (
              <div className="flex gap-3">
                <button
                  className="py-1.5 px-4 rounded-md text-sm font-medium bg-red-950 border border-red-800 text-red-200 hover:bg-red-900 transition-colors"
                  onClick={() => changeStatus("rejected")}
                >
                  Reject
                </button>
                <button
                  className="py-1.5 px-4 rounded-md text-sm font-medium bg-green-950 border border-green-800 text-green-200 hover:bg-green-900 transition-colors"
                  onClick={() => changeStatus("approved")}
                >
                  Approve
                </button>
              </div>
            ) : (
              <p className="text-sm text-gray-400">
                Decision:{" "}
                <span className={statusClass(currentTicket.status)}>
                  {currentTicket.status.charAt(0).toUpperCase() +
                    currentTicket.status.slice(1)}
                </span>
              </p>
            )}
          </div>
        </div>
    </div>
  );
};
