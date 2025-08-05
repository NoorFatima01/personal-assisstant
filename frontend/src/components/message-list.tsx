
const MessageList = ({messages} : {messages: {role:string, content:string}[]}) => {
  return (
     <div className="mb-4 space-y-2 max-h-[60vh] overflow-y-auto">
    {messages.map((msg, idx) => (
      <div
        key={idx}
        className={`p-2 rounded-xl text-sm whitespace-pre-wrap ${
          msg.role === "user" ? "bg-blue-100 text-left" : "bg-gray-100 text-left"
        }`}
      >
        {msg.content}
      </div>
    ))}
  </div>

  )
}

export default MessageList