import React, { useEffect, useRef } from "react";
import { type Message } from "../lib/types";

interface MessageListProps {
  messages: Message[];
  isStreaming?: boolean;
}

const MessageList: React.FC<MessageListProps> = ({
  messages,
  isStreaming = false,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
          <svg
            className="w-8 h-8 text-blue-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Start Your Conversation
        </h3>
        <p className="text-gray-600 max-w-sm">
          Ask me anything about your documents. I'm here to help you analyze and
          understand your data.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto max-h-[70vh] px-1">
      <div className="space-y-6">
        {messages.map((message, index) => (
          <div key={index} className="space-y-4">
            {/* User Message */}
            <div className="flex justify-end">
              <div className="max-w-[80%] group">
                <div className="flex items-end space-x-2">
                  <div className="bg-blue-600 text-white p-4 rounded-2xl rounded-br-md shadow-sm">
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                      {message.user_input}
                    </p>
                  </div>
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg
                      className="w-4 h-4 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                </div>
                <div className="text-xs text-gray-500 mt-1 text-right">
                  You • Just now
                </div>
              </div>
            </div>

            {/* Assistant Message */}
            {(message.assistant_response || isStreaming) && (
              <div className="flex justify-start">
                <div className="max-w-[80%] group">
                  <div className="flex items-end space-x-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <svg
                        className="w-4 h-4 text-white"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div className="bg-white border border-gray-200 p-4 rounded-2xl rounded-bl-md shadow-sm">
                      {message.assistant_response ? (
                        <p className="text-sm leading-relaxed whitespace-pre-wrap text-gray-800">
                          {message.assistant_response}
                        </p>
                      ) : isStreaming && index === messages.length - 1 ? (
                        <div className="flex items-center space-x-2">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div
                              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.1s" }}
                            ></div>
                            <div
                              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.2s" }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-500">
                            AI is thinking...
                          </span>
                        </div>
                      ) : null}
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 mt-1 ml-10">
                    AI Assistant •{" "}
                    {message.assistant_response ? "Just now" : "Typing..."}
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
