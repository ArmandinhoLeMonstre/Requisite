import { useState } from "react";
import { createTicket, sendMessage } from "../api/client";
import { useNavigate } from "react-router-dom";

export function NewTicketPage() {
  const [inputMessage, setInputMessage] = useState("");
  const navigate = useNavigate();

  async function StartTicket() {
    try {
		const ticket = await createTicket();
		await sendMessage(ticket.id, inputMessage);
		navigate(`/ticket/${ticket.id}`);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="flex-1 flex flex-col items-center bg-gray-950 gap-6 px-4 pt-70">
      <div className="flex flex-col items-center gap-2 mb-2">
        <h1 className="text-white text-5xl font-semibold tracking-tight">
          Requisite
        </h1>
        <p className="text-gray-400 text-sm text-center max-w-md">
          Submit an equipment request and our AI will check inventory, find the
          best options, and handle the rest — so you can focus on your work.
        </p>
      </div>
      <div className="w-full max-w-xl">
        <div className="flex flex-col bg-gray-800 rounded-3xl px-5 py-4 gap-4">
          <input
            type="text"
            autoFocus
            placeholder="I need a new keyboard, a monitor stand..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => {
              if (
                e.key === "Enter" &&
                inputMessage &&
                inputMessage.trim() !== ""
              ) {
                StartTicket();
                setInputMessage("");
              }
            }}
            className="bg-transparent text-white placeholder-gray-500 outline-none text-base w-full"
          />
          <div className="flex justify-end">
            <button
              disabled={!inputMessage}
              onClick={StartTicket}
              className="text-white bg-gray-600 hover:bg-gray-500 rounded-full px-5 py-1.5 text-sm disabled:hover:bg-gray-600"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
