function MessageInput({ inputMessage, setInputMessage, addMessage }) {

  return (
    <div className="flex-col-reverse border rounded-3xl p-4">
      <input
        type="text"
        placeholder="Write a message..."
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
      />
      <button type="submit" onClick={() => {addMessage(inputMessage); setInputMessage("");}}>
        Send
      </button>
    </div>
  );
}

export default MessageInput;
