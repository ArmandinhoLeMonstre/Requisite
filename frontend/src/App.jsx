import { useState } from "react";
import Sidebar from "./components/SideBar";
import ChatWindow from "./components/ChatWindow";

function App() {
  const [tickets, setTickets] = useState([
    {
      id: 1,
      title: "Need a new keyboard",
      messages: [
        {id: 1, role: "user", content: "I want a new keyboard"},
        {id: 2, role: "Agent", content: "Get it yourself ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL ZEMEL "},
        {id: 3, role: "user", content: "Zemell ? :("},
        {id: 4, role: "Agent", content: "Tarlouzeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee tu penses faire quoi"},
      ],
    },
    { id: 2, title: "Monitor replacement", messages: [] },
  ]);
  const [activeTicketId, setActiveTicketId] = useState(null);
  const activeTicket = tickets.find(ticket => ticket.id === activeTicketId) || null;

  function addMessage(message ) {
    setTickets((prev) =>
      prev.map((ticket) => {
        if (ticket.id === activeTicket.id) {
          return { ...ticket, messages: [...ticket.messages, {id: ticket.messages.length + 1, role: "user", content: message} ] };
        }
        return ticket;
      }),
    );
  }

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar tickets={tickets} onTicketClick={setActiveTicketId} />
      {activeTicket ? (
        <ChatWindow activeTicket={activeTicket} addMessage={addMessage} />
      ) : (
        <ChatWindow activeTicket={null} addMessage={addMessage} />
      )}
    </div>
  );
}

export default App;
