import React from "react";
import MessageList from "../components/message-list";
import { fetchLLMResponseStream, fetchChatSession } from "../utils/api-client";
import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { getUserProfile } from "../utils/api-client";
import ChatInputForm from "../form/chat-input-form";
import toast from "react-hot-toast";
import Loader from "../components/loader";

const Chat = () => {
  const [messages, setMessages] = React.useState<
    { user_input: string; assistant_response: string }[]
  >([]);
  const [loading, setLoading] = React.useState(false);
  const { chatId } = useParams<{ chatId: string }>();
  const [weeks, setWeeks] = useState<string[]>([]);
  const [abortController, setAbortController] =
    useState<AbortController | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchSession = async () => {
      if (!chatId) return;
      setIsLoading(true);
      try {
        const session = await fetchChatSession({ chatId });
        console.log("Fetched chat session:", session);
        if (Array.isArray(session)) {
          setMessages([]);
        } else {
          setMessages(session?.messages || []);
        }
      } catch (err) {
        toast.error(`Error fetching chat session: ${err instanceof Error ? err.message : String(err)}`);
      } finally {
        setIsLoading(false);
      }
    };
    fetchSession();
  }, [chatId]);

  useEffect(() => {
    const fetchUserProfile = async () => {
      setIsLoading(true);
      try {
        const profile = await getUserProfile();
        setWeeks(profile.weeks || []);
        console.log("Weeks are:", profile.weeks);
      } catch (err) {
        toast.error(
          `Error fetching user profile: ${
            err instanceof Error ? err.message : String(err)
          }`
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  const onDone = () => {
    setIsStreaming(false);
    setAbortController(null);
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
          ? { ...msg, assistant_response: msg.assistant_response + token }
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
  };

  const handleSend = async (question: string, weeks: string[]) => {
    const controller = new AbortController();
    setAbortController(controller);
    setIsStreaming(true);
    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { user_input: question, assistant_response: "" },
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

  if (isLoading) {
    return <Loader />;
  }

  if(weeks.length === 0) {
    return <div>Looks like you have not uploaded any documents yet. Please upload documents to get started.</div>;
  }

  return (
    <div>
      <h2>The chat page</h2>
      <div className="p-4 max-w-2xl mx-auto">
        <MessageList messages={messages} />
        <ChatInputForm
          onSend={handleSend}
          loading={loading}
          weeks={weeks}
          isStreaming={isStreaming}
        />
        {isStreaming && (
          <button
            onClick={endStreaming}
            className="mt-4 text-white px-4 py-2 rounded"
          >
            End Streaming
          </button>
        )}
      </div>
    </div>
  );
};

export default Chat;
