export interface Message {
  user_input: string;
  assistant_response: string;
}

export interface ChatInputFormData {
  question: string;
  weeks: string[];
}

export interface ChatInputFormProps {
  weeks: string[];
  loading: boolean;
  onSend: (input: string, weeks: string[]) => void;
  isStreaming: boolean;
}

export interface ChatState {
  messages: Message[];
  loading: boolean;
  isStreaming: boolean;
  isLoading: boolean;
  abortController: AbortController | null;
}

export interface StreamingCallbacks {
  onToken: (token: string) => void;
  onDone: () => void;
  onError: (error: unknown) => void;
}
