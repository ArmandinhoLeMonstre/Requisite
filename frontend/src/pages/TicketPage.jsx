import { useEffect, useRef, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import ChatWindow from "../components/ChatWindow";
import { getChats, sendMessage } from "../api/client";

export function TicketPage() {
  const { ticketId } = useParams();
  const [loading, setLoading] = useState(false);
  const { state } = useLocation();
  const hasRun = useRef(false)
  const [ticketInfo, setTicketInfo] = useState(
    state?.firstMessage
      ? { chats: [{ sender: "user", message: state.firstMessage, id: 0 }] }
      : null,
  );

  async function addMessage(message, optimistic = true) {
    if (optimistic) {
      setTicketInfo({
        ...ticketInfo,
        chats: [
          ...ticketInfo.chats,
          { sender: "user", message, id: ticketInfo.chats.length + 1 },
        ],
      });
    }
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
  if (state?.firstMessage && !hasRun.current) {
    hasRun.current = true
    addMessage(state.firstMessage, false)
  }
}, [])

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getChats(ticketId);
        setTicketInfo(data);
      } catch (error) {
        console.error("Failed to load ticket infos", error);
      }
    }
    if (!state?.firstMessage) {
      fetchData();
    }
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
