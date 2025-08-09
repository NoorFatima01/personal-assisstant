// components/Chat.tsx
import React from "react";
import { useParams } from "react-router-dom";
import { useChat } from "../hooks/use-chat";
import ChatInputForm from "../form/chat-input-form";
import MessageList from "../components/message-list";
import Loader from "../components/loader";
import EmptyState from "../components/empty-chat-state";
import StreamingControls from "../components/streaming-controls";
import ChatHeader from "../components/chat-header";

const Chat: React.FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const {
    messages,
    loading,
    isStreaming,
    isLoading,
    weeks,
    handleSend,
    endStreaming,
  } = useChat(chatId);

  if (isLoading) {
    return <Loader />;
  }

  if (weeks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className=" bg-gray-50">
      {/* Header */}
      <ChatHeader />

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {/* Messages */}
        <div className="space-y-4 my-8">
          <MessageList messages={messages} />
        </div>

        {/* Input Form */}
        <div className="">
          <ChatInputForm
            onSend={handleSend}
            loading={loading}
            weeks={weeks}
            isStreaming={isStreaming}
          />

          {/* Streaming Controls */}
          <StreamingControls
            isStreaming={isStreaming}
            onEndStreaming={endStreaming}
          />
        </div>
      </div>
    </div>
  );
};

export default Chat;
