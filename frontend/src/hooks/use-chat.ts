import { useState, useEffect, useCallback } from "react";
import { toast } from "react-hot-toast";
import { type Message } from "../lib/types";
import {
  fetchChatSession,
  fetchLLMResponseStream,
  getUserProfile,
} from "../utils/api-client";

export const useChat = (chatId?: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [weeks, setWeeks] = useState<string[]>([]);
  const [abortController, setAbortController] =
    useState<AbortController | null>(null);

  // Fetch chat session
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
        toast.error(
          `Error fetching chat session: ${
            err instanceof Error ? err.message : String(err)
          }`
        );
      } finally {
        setIsLoading(false);
      }
    };
    fetchSession();
  }, [chatId]);

  // Fetch user profile and weeks
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

  // Streaming callbacks
  const onDone = useCallback(() => {
    setIsStreaming(false);
    setAbortController(null);
  }, []);

  const onError = useCallback((error: unknown) => {
    setIsStreaming(false);
    setAbortController(null);
    toast.error(
      `Error generating response: ${
        error instanceof Error ? error.message : String(error)
      }`
    );
    console.error("Error generating response:", error);
  }, []);

  const onToken = useCallback((token: string) => {
    setMessages((prev) =>
      prev.map((msg, index) =>
        index === prev.length - 1
          ? { ...msg, assistant_response: msg.assistant_response + token }
          : msg
      )
    );
  }, []);

  // Handle message sending
  const handleSend = useCallback(
    async (question: string, selectedWeeks: string[]) => {
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
          weeks: selectedWeeks,
          chatId: chatId || "",
          onToken,
          onDone,
          onError,
        });
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
        setIsStreaming(false);
        setAbortController(null);
      }
    },
    [chatId, onToken, onDone, onError]
  );

  // End streaming
  const endStreaming = useCallback(() => {
    if (abortController) {
      abortController.abort();
      setAbortController(null);
    }
    setIsStreaming(false);
  }, [abortController]);

  return {
    messages,
    loading,
    isStreaming,
    isLoading,
    weeks,
    handleSend,
    endStreaming,
  };
};
