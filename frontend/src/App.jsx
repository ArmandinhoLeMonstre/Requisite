import { useState } from "react";
import Sidebar from "./components/SideBar";
import ChatWindow from "./components/ChatWindow";

function App() {
  const [tickets, setTickets] = useState([
    { id: 1, title: "Need a new keyboard" },
    { id: 2, title: "Monitor replacement" },
  ]);
  const [activeTicket, setActiveTicket] = useState(null);

  return (
    <div className="flex h-screen bg-gray-100">
        <Sidebar tickets={tickets} onTicketClick={setActiveTicket} />
        <ChatWindow activeTicket={activeTicket} />
    </div>
  );
}

export default App;
