function MessageInput({ inputMessage, setInputMessage, addMessage, loading }) {
  return (
    <div className=" m-3.5">
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
          className="flex-1 bg-transparent text-white placeholder-gray-500 outline-none "
        />
        <button
          onClick={() => {
            if (inputMessage && inputMessage.trim() !== "") {
              addMessage(inputMessage);
              setInputMessage("");
            }
          }}
          disabled={loading}
          className="text-white bg-gray-600 hover:bg-gray-500 rounded-full px-4 py-1 text-sm disabled:hover:bg-gray-600 disabled:cursor-not-allowed"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default MessageInput;
