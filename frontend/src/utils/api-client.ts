import axios from "axios";
import { supabase } from "../lib/supabase";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const getUserProfile = async () => {
  try {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session?.access_token) {
      throw new Error("No authentication token found");
    }

    console.log("Fetching user profile with token:", session.access_token);

    const response = await axios.get(`${baseURL}/api/users/me`, {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });

    return response.data;
  } catch (error) {
    console.error("Failed to fetch user profile:", error);
    throw error;
  }
};

export const uploadPDF = async (formData: FormData) => {
  try {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session?.access_token) {
      throw new Error("No authentication token found");
    }

    const response = await axios.post(
      `${baseURL}/api/docs/upload_doc`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${session.access_token}`,
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Upload failed:", error);
    throw error;
  }
};

// TODO: refactor this to use a hook or something
export async function fetchLLMResponseStream({
  question,
  weeks,
  chatId,
  onToken,
  onDone,
  onError,
  abortController,
}: {
  question: string;
  weeks: string[];
  chatId: string;
  onToken: (token: string) => void;  // Called as each token arrives
  onDone?: () => void;               // Optional: called after stream ends
  onError?: (err: Error) => void;    // Optional: error handling
  abortController?: AbortController; // Optional: to cancel the request
}) {
  try {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session?.access_token) {
      throw new Error("No authentication token found");
    }
    console.log("Fetching LLM response stream with token:", session.access_token);

    const response = await fetch(`${baseURL}/api/qa/ask-stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.access_token}`,
      },
      signal: abortController?.signal,
      body: JSON.stringify({
        question,
        chat_id: chatId,
        week_start: weeks,
      }),
    });

    if (!response.ok || !response.body) {
      const errorText = await response.text();
      console.error("LLM stream error:", errorText);
      throw new Error(`Stream request failed: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split("\n\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const token = line.replace("data: ", "").replace(/\\n/g, "\n").trim();
          if (token) onToken(token);
        }
      }
    }

    if (onDone) onDone();
  } catch (err: unknown) {
    console.error("Streaming fetch failed:", err);
    if (onError) onError(err instanceof Error ? err : new Error(String(err)));
    else throw err;
  }
}


