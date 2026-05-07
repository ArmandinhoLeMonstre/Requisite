import { useState, useEffect } from "react";
import Sidebar from "./components/SideBar";
import ChatWindow from "./components/ChatWindow";
import { getChats, createTicket, getTickets, sendMessage } from "./api/client";


localStorage.setItem("token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzc4MTg0MzAwfQ.RzXQL47EJ-YW3FlzTwk8u_eBpzDB-oY1KSW6v0mAHIk") 
// localStorage.removeItem('token')

function App() {
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
        if (!activeTicket) return
        const data = await getChats(activeTicket.id);
        setTicketInfo(data);
      } catch (error) {
        console.error("Failed to load ticket infos", error);
      }
    }
    fetchData();
  }, [activeTicket]);

  function addMessage(message) {
    sendMessage(activeTicket.id, message)
  }

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar tickets={tickets} onTicketClick={setActiveTicketId} />
      {activeTicket ? (
        <ChatWindow activeTicket={ticketInfo} addMessage={addMessage} />
      ) : (
        <ChatWindow activeTicket={null} addMessage={addMessage} />
      )}
    </div>
  );
}

export default App;
