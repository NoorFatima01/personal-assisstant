import { useEffect, useState, useCallback } from "react";
import { fetchUserChats } from "../utils/api-client";
import type { ChatType } from "../lib/schemas";
import toast from "react-hot-toast";

export const useUserChats = (userId: string) => {
  const [userChats, setUserChats] = useState<ChatType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchChats = useCallback(async () => {
    if (!userId) return;

    setIsLoading(true);
    setError(null);

    try {
      const chats = await fetchUserChats();
      setUserChats(chats);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to fetch chats";
      setError(errorMessage);
      toast.error(`Error fetching chats: ${errorMessage}`);
      console.error("Error fetching user chats:", err);
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  // Initial fetch
  useEffect(() => {
    fetchChats();
  }, [fetchChats]);
  return {
    userChats,
    isLoading,
    error,
  };
};
