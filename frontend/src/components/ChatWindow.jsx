
function ChatWindow({activeTicket}) {
	return (
	<div className="flex-1 flex flex-col-reverse">
		{ activeTicket ? (
			<div className="flex-1">
				<p className="align-middle">{activeTicket.title}</p>
			</div>
		) : (
			<div className="flex-1">
				<p>Select a ticket or start a new one</p>
			</div>
		)}
        {/* <div className="flex-col-reverse p-5 border rounded-3xl">
          <p className="text-gray-400 text-lg">chat...</p>
        </div>
		<div className="flex-1 ">
			<p className="text-black text-lg"> salut</p>
		</div> */}
      </div>
	);
}

export default ChatWindow