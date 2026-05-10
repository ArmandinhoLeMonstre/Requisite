import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ChatWindow from "../components/ChatWindow";
import { getChats, sendMessage } from "../api/client";

export function TicketPage() {
  const { ticketId } = useParams();
  const [loading, setLoading] = useState(false);
  const [ticketInfo, setTicketInfo] = useState(null);

  async function addMessage(message) {
    setTicketInfo({
      ...ticketInfo,
      chats: [
        ...ticketInfo.chats,
        { sender: "user", message, id: ticketInfo.chats.length + 1 },
      ],
    });
    setLoading(true);
    try {
      await sendMessage(ticketId, message);
      const data = await getChats(ticketId);
      setTicketInfo(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getChats(ticketId);
        setTicketInfo(data);
      } catch (error) {
        console.error("Failed to load ticket infos", error);
      }
    }
    fetchData();
  }, [ticketId]);

  return (
    <div className="flex-1 flex justify-center h-screen bg-gray-950 overflow-hidden ">
      <ChatWindow
        activeTicket={ticketInfo}
        addMessage={addMessage}
        loading={loading}
      />
    </div>
  );
}
