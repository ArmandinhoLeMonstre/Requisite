import { useEffect, useState } from "react";
import { getTickets } from "../api/client";
import Sidebar from "./SideBar";
import { Outlet } from "react-router-dom";

export function ChatLayout() {
  const [tickets, setTickets] = useState([]);

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

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar tickets={tickets} />
      <Outlet />
    </div>
  );
}
