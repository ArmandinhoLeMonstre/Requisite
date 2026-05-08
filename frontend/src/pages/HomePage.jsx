import { useState, useEffect } from "react";
import Sidebar from "../components/SideBar";
import ChatWindow from "../components/ChatWindow";
import { getChats, getTickets, sendMessage } from "../api/client";

export function HomePage() {
  const [loading, setLoading] = useState(false);
  const [tickets, setTickets] = useState([]);
  const [ticketInfo, setTicketInfo] = useState(null);
  const [activeTicketId, setActiveTicketId] = useState(null);
  const activeTicket =
    tickets.find((ticket) => ticket.id === activeTicketId) || null;

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getTickets();
        setTickets(data);
      } catch (error) {
        console.error("Failed to load tickets:", error);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    async function fetchData() {
      try {
        if (!activeTicket) return;
        const data = await getChats(activeTicket.id);
        setTicketInfo(data);
      } catch (error) {
        console.error("Failed to load ticket infos", error);
      }
    }
    fetchData();
  }, [activeTicket]);

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
      await sendMessage(activeTicket.id, message);
      const data = await getChats(activeTicket.id);
      setTicketInfo(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar tickets={tickets} onTicketClick={setActiveTicketId} />
      {activeTicket ? (
        <ChatWindow
          activeTicket={ticketInfo}
          addMessage={addMessage}
          loading={loading}
        />
      ) : (
        <ChatWindow activeTicket={null} addMessage={addMessage} />
      )}
    </div>
  );
}

