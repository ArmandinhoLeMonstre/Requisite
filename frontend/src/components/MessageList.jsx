function MessageList({ listMessage }) {
  return (
    <div className="h-14/15">
      {listMessage.length > 0 ? (
        listMessage.map((message) => (
          <div className={message.role === "User" ? "w-auto p-1 flex justify-end rounded border" : "styles for agent"}>
            <h2 key={message.id} className="justify-end">
              {message.content}
            </h2>
          </div>
        ))
      ) : (
        <h2>No messages</h2>
      )}
    </div>
  );
}

export default MessageList;
