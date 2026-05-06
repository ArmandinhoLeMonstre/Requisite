import { useState } from "react";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

function ChatWindow({ activeTicket, addMessage }) {
  const [inputMessage, setInputMessage] = useState("");
  
  return (
    <div className="flex-1 flex ">
      {activeTicket ? (
        <div className="flex-1">
          <MessageList listMessage={activeTicket.messages} />
          <MessageInput
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            addMessage={addMessage}
          />
        </div>
      ) : (
        <div className="flex-1">
          <p>Select a ticket or start a new one</p>
        </div>
      )}
    </div>
  );
}

export default ChatWindow;
