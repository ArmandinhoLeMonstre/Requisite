import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

function MessageList({ listMessage }) {
  const bottomPanelRef = useRef(null);

  useEffect(() => {
    if (bottomPanelRef.current) {
      bottomPanelRef.current.scrollIntoView();
    }
  }, [listMessage]);
  
  return (
    <div className="flex flex-col gap-3 p-4 overflow-y-auto flex-1">
      {listMessage.length > 0 ? (
        listMessage.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            {message.sender === "user" ? (
              <p className="px-4 py-2 rounded-2xl bg-gray-700 text-white max-w-4/5 break-words">
                {message.message}
              </p>
            ) : (
              <div className="text-gray-300 w-full break-words prose prose-invert prose-sm max-w-none">
                <ReactMarkdown>{message.message}</ReactMarkdown>
              </div>
            )}
          </div>
        ))
      ) : (
        <p className="text-gray-500 text-sm">No messages yet</p>
      )}
      <div ref={bottomPanelRef} />
    </div>
  );
}

export default MessageList;
