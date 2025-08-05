import React from "react";
import MessageList from "../components/message-list";
import { fetchLLMResponseStream } from "../utils/api-client";
import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { getUserProfile } from "../utils/api-client";
import ChatInputForm from "../form/chat-input-form";
import toast from "react-hot-toast";

const Chat = () => {
  const [messages, setMessages] = React.useState<
    { role: string; content: string }[]
  >([]);
  const [loading, setLoading] = React.useState(false);
  const { chatId } = useParams<{ chatId: string }>();
  const [weeks, setWeeks] = useState<string[]>([]);
  const [abortController, setAbortController] = useState<AbortController | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);


  useEffect(() => {
    getUserProfile()
      .then((profile) => setWeeks(profile.weeks || []))
      .catch((err) => console.error("Error fetching user profile:", err));
  }, []);

  const onDone = () => {
    setIsStreaming(false);
    setAbortController(null);
    toast.success("Response generated successfully!");
  };

  const onError = (error: unknown) => {
    setIsStreaming(false);
    setAbortController(null);
    toast.error(
      `Error generating response: ${
        error instanceof Error ? error.message : String(error)
      }`
    );
    console.error("Error generating response:", error);
  };

  const onToken = (token: string) => {
    setMessages((prev) =>
      prev.map((msg, index) =>
        index === prev.length - 1
          ? { ...msg, content: msg.content + token }
          : msg
      )
    );
  };

  const endStreaming = () => {
    if (abortController) {
      abortController.abort();
      setAbortController(null);
    }
    setIsStreaming(false);
  }

  const handleSend = async (question: string, weeks: string[]) => {
    const controller = new AbortController();
    setAbortController(controller);
    setIsStreaming(true);
    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { role: "user", content: question },
      { role: "assistant", content: "" },
    ]);

    try {
      await fetchLLMResponseStream({
        question,
        weeks,
        chatId: chatId || "",
        onToken: onToken,
        onDone: onDone,
        onError: onError,
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      setIsStreaming(false);
      setAbortController(null);
    }
  };

  return (
    <div>
      <div className="p-4 max-w-2xl mx-auto">
        <MessageList messages={messages} />
        <ChatInputForm onSend={handleSend} loading={loading} weeks={weeks} isStreaming={isStreaming} />
        {isStreaming && (
          <button onClick={endStreaming} className="mt-4 bg-red-500 text-white px-4 py-2 rounded">
            End Streaming
          </button>
        )}
      </div>
    </div>
  );
};

export default Chat;
