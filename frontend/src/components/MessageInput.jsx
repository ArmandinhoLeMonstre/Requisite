function MessageInput({
  ticketData,
  inputMessage,
  setInputMessage,
  addMessage,
  loading,
}) {
  if (ticketData?.status)
    return (
      <div className="mx-4 m-1">
        <div className="flex items-center justify-center gap-2 rounded-2xl px-4 py-3">
          <span
            className={`text-l font-medium px-2 py-0.5 rounded-full ${
              ticketData.status === "approved"
                ? "bg-green-950 border border-green-800 text-green-300"
                : ticketData.status === "rejected"
                  ? "bg-red-950 border border-red-800 text-red-300"
                  : "bg-amber-950 border border-amber-800 text-amber-300"
            }`}
          >
            {ticketData.status === "pending"
              ? "Waiting for manager approval"
              : ticketData.status === "approved"
                ? "Request approved"
                : "Request rejected"}
          </span>
        </div>
      </div>
    );

  return (
    <div className="mx-4 mb-4">
      <div className="flex items-center gap-2 bg-gray-800 rounded-3xl px-4 py-3">
        <input
          autoFocus
          type="text"
          placeholder="Write a message..."
          disabled={loading}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => {
            if (
              e.key === "Enter" &&
              inputMessage &&
              inputMessage.trim() !== ""
            ) {
              addMessage(inputMessage);
              setInputMessage("");
            }
          }}
          className="flex-1 bg-transparent text-white placeholder-gray-500 outline-none text-sm"
        />
        {loading ? (
          <div className="w-5 h-5 rounded-full border-2 border-gray-600 border-t-green-500 animate-spin flex-shrink-0" />
        ) : (
          <button
            onClick={() => {
              if (inputMessage && inputMessage.trim() !== "") {
                addMessage(inputMessage);
                setInputMessage("");
              }
            }}
            disabled={loading}
            className="text-white bg-gray-600 hover:bg-gray-500 rounded-full px-4 py-1 text-sm disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex-shrink-0"
          >
            Send
          </button>
        )}
      </div>
    </div>
  );
}

export default MessageInput;
