import { useEffect, useState } from "react";
import { getMe, getTickets } from "../api/client";
import Sidebar from "./SideBar";
import { Outlet } from "react-router-dom";

export function ChatLayout() {
  const [tickets, setTickets] = useState([]);
  const [user, setUser] = useState(null);

  async function refreshTickets() {
    try {
      const data = await getTickets();
      setTickets(data);
    } catch (error) {
      console.error("Failes to load tickets: ", error);
    }
  }

  async function getUser() {
    try {
      const res = await getMe();
      setUser(res.data);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    refreshTickets();
    getUser();
  }, []);

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar tickets={tickets} user={user} />
      <Outlet context={{ refreshTickets }} />
    </div>
  );
}
