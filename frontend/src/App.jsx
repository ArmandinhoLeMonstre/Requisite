import { useState } from "react";
import Sidebar from "./components/SideBar";

function App() {
  const [tickets, setTickets] = useState([
  { id: 1, title: "Need a new keyboard" },
  { id: 2, title: "Monitor replacement" },
])
const [activeTicket, setActiveTicket] = useState(null)

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar tickets={tickets} onTicketClick={setActiveTicket}/>
      console.log(activeTicket)
      {/* Chat area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 p-6">
          <p className="text-gray-400">Select a ticket or start a new one</p>
        </div>
      </div>
    </div>
  );
}

export default App;
