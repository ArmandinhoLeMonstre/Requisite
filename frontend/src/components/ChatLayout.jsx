import { useEffect, useState } from "react";
import { getTickets } from "../api/client";
import Sidebar from "./SideBar";
import { Outlet } from "react-router-dom";

export function ChatLayout() {
  const [tickets, setTickets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  async function refreshTickets() {
    try {
      const data = await getTickets();
      setTickets(data);
    } catch (error) {
      console.error("Failed to load tickets: ", error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    refreshTickets();
  }, []);

  if (isLoading)
    return (
      <div className="flex h-screen items-center justify-center bg-gray-950">
        <div className="w-6 h-6 rounded-full border-2 border-gray-600 border-t-white animate-spin" />
      </div>
    );
  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar tickets={tickets} />
      <Outlet context={{ refreshTickets }} />
    </div>
  );
}
