import { useState } from "react";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

function ChatWindow({ activeTicket, addMessage, loading }) {
  const [inputMessage, setInputMessage] = useState("");

  return (
    <div className="flex-1 flex flex-col bg-gray-950 overflow-hidden">
      {activeTicket ? (
        <div className="flex-1 flex flex-col max-w-3xl w-full mx-auto overflow-hidden">
          <MessageList listMessage={activeTicket.chats} />
          <MessageInput
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            addMessage={addMessage}
            loading={loading}
          />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center">
          <p className="text-gray-500">Select a ticket or start a new one</p>
        </div>
      )}
    </div>
  );
}

export default ChatWindow;
