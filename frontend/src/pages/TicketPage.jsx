import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ChatWindow from "../components/ChatWindow";
import { getChats, sendMessage } from "../api/client";
import toast from "react-hot-toast";

export function TicketPage() {
  const navigate = useNavigate()
  const { ticketId } = useParams();
  const [loadingMap, setLoadingMap] = useState({});
  const [ticketsData, setTicketsData] = useState({});

  const loading = loadingMap[ticketId] ?? false;
  const ticketInfo = ticketsData[ticketId] ?? null;

  async function addMessage(message) {
    const id = ticketId;
    setTicketsData((prev) => ({
      ...prev,
      [id]: {
        ...prev[id],
        chats: [
          ...prev[id].chats,
          { sender: "user", message, id: Date.now() },
        ],
      },
    }));
    setLoadingMap((prev) => ({ ...prev, [id]: true }));
    try {
      await sendMessage(id, message);
      const data = await getChats(id);
      setTicketsData((prev) => ({ ...prev, [id]: data }));
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingMap((prev) => ({ ...prev, [id]: false }));
    }
  }

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getChats(ticketId);
        setTicketsData((prev) => ({ ...prev, [ticketId]: data }));
      } catch (error) {
        if (error.status === 422 || error.status === 404){
          toast.error("Ticket not found");
          navigate("/new")
          return ;
        }
        console.error("Failed to load ticket infos", error);

      }
    }
    fetchData();
  }, [ticketId]);

  return (
    <div className="flex-1 flex justify-center h-screen bg-gray-950 overflow-hidden">
      <ChatWindow
        activeTicket={ticketInfo}
        addMessage={addMessage}
        loading={loading}
      />
    </div>
  );
}
