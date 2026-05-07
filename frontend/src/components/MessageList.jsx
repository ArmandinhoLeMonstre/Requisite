import { useEffect, useRef } from "react";

function MessageList({ listMessage }) {
const bottomPanelRef = useRef(null);

useEffect(() => {
	if (bottomPanelRef.current) {
		bottomPanelRef.current.scrollIntoView();
	}
}, [listMessage])

  return (
    <div className="flex flex-col gap-3 p-4 overflow-y-auto flex-1">
      {listMessage.length > 0 ? (
        listMessage.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
          >
            {message.role === "user" ? (
              <p className="px-4 py-2 rounded-2xl bg-gray-700 text-white max-w-4/5 break-words">
                {message.content}
              </p>
            ) : (
              <p className="text-gray-300 w-full break-words">
                {message.content}
              </p>
            )}
          </div>
        ))
      ) : (
        <p className="text-gray-500 text-sm">No messages yet</p>
      )}
	  <div ref={bottomPanelRef}> </div>
    </div>
  );
}

export default MessageList;
