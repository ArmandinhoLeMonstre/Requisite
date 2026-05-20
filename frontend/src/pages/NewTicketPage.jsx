import { useEffect, useState } from "react";
import { createTicket, getMe, joinGroup, sendMessage } from "../api/client";
import { useNavigate, useOutletContext } from "react-router-dom";

export function NewTicketPage() {
  const [inputMessage, setInputMessage] = useState("");
  const [user, setUser] = useState(null);
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);
  const navigate = useNavigate();
  const { refreshTickets } = useOutletContext();

  async function StartTicket() {
    try {
      const ticket = await createTicket(inputMessage);
      refreshTickets();
      await sendMessage(ticket.id, inputMessage);
      navigate(`/ticket/${ticket.id}`, {
        state: { firstMessage: inputMessage },
      });
    } catch (error) {
      console.error(error);
    }
  }

  async function submitCode() {
    try {
      const res = await joinGroup(user.id, code);
      setUser(res.data);
    } catch (error) {
      console.log(error);
      if (error.status === 404) {
        setErrorMessage("Invalid Code");
      }
    }
  }

  useEffect(() => {
    async function getUser() {
      try {
        const res = await getMe();
        setUser(res.data);
      } catch (error) {
        console.error(error);
      }
    }
    getUser();
  }, []);

  if (!user?.group_id) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-gray-950 gap-4 px-4">
        <div className="flex flex-col items-center gap-2 mb-4 text-center">
          <h1 className="text-white text-3xl font-semibold tracking-tight">
            Join a group
          </h1>
          <p className="text-gray-400 text-sm max-w-sm">
            You need to join a group before you can submit equipment requests.
            Ask your manager for the group code.
          </p>
        </div>
        <div className="w-full max-w-xs flex flex-col gap-3">
          {errorMessage && (
            <p className="text-red-400 text-xs text-center">{errorMessage}</p>
          )}
          <input
            type="text"
            placeholder="Enter group code (e.g. 4F3DY)"
            maxLength={5}
            value={code}
            onChange={(e) => setCode(e.target.value.toUpperCase())}
            className="bg-gray-800 text-white placeholder-gray-500 outline-none rounded-xl px-4 py-3 text-sm tracking-widest text-center"
          />
          <button
            disabled={code.length !== 5}
            onClick={() => submitCode()}
            className="text-white bg-gray-700 hover:bg-gray-600 rounded-xl py-2.5 text-sm disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Join
          </button>
        </div>
      </div>
    );
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
