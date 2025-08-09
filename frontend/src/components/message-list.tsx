
const MessageList = ({messages} : {messages: {user_input:string, assistant_response:string}[]}) => {
  return (
     <div className="mb-4 space-y-2 max-h-[60vh] overflow-y-auto">
   {messages.length > 0 ? (
      messages.map((msg, idx) => (
        <div
          key={idx}
        >
          <p className={`p-2 rounded-xl text-sm whitespace-pre-wrap bg-blue-100 text-left`}>
            {msg.user_input}
          </p>
          <p className={`p-2 rounded-xl text-sm whitespace-pre-wrap bg-green-100 text-left`}>
            {msg.assistant_response}
          </p>
        </div>
      ))
    ) : (
      <p>Start a conversation</p>
    )}
  </div>

  )
}

export default MessageList