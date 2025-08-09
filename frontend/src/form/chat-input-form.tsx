import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { type ChatInputFormProps, type ChatInputFormData } from "../lib/types";
import { sortWeeks } from "../utils/chat-utils";
import { validateChatInput } from "../utils/chat-utils";
import { chatInputFormSchema } from "../lib/schemas";
import WeekSelector from "../components/week-selector";

const ChatInputForm: React.FC<ChatInputFormProps> = ({
  weeks,
  loading,
  onSend,
  isStreaming,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    setValue,
    watch,
  } = useForm<ChatInputFormData>({
    resolver: zodResolver(chatInputFormSchema),
    defaultValues: {
      weeks: [],
      question: "",
    },
  });

  const selectedWeeks = watch("weeks") || [];
  const question = watch("question") || "";

  const onSubmit = (data: ChatInputFormData) => {
    if (!validateChatInput(data)) return;
    const sortedWeeks = sortWeeks(data.weeks);
    onSend(data.question, sortedWeeks);
    reset();
  };

  const isDisabled = loading || isSubmitting;

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Question Input */}
        <div className="space-y-2">
          <label
            htmlFor="question"
            className="block text-sm font-semibold text-gray-700"
          >
            Your Question
          </label>
          <div className="relative">
            <textarea
              id="question"
              rows={3}
              className={`
                w-full px-4 py-3 border-2 rounded-lg resize-none transition-all duration-200
                focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                ${
                  errors.question
                    ? "border-red-300 focus:ring-red-500 focus:border-red-500"
                    : "border-gray-300"
                }
                ${isDisabled ? "bg-gray-50 cursor-not-allowed" : "bg-white"}
              `}
              placeholder="Ask me anything about your selected weeks..."
              {...register("question")}
              disabled={isDisabled}
            />
            <div className="absolute bottom-2 right-2 text-xs text-gray-400">
              {question.length}/500
            </div>
          </div>
          {errors.question && (
            <p className="text-red-500 text-sm mt-1 flex items-center">
              <svg
                className="w-4 h-4 mr-1"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
              {errors.question.message}
            </p>
          )}
        </div>

        {/* Week Selection */}
        <WeekSelector
          weeks={weeks}
          selectedWeeks={selectedWeeks}
          setValue={setValue}
          error={Array.isArray(errors.weeks) ? errors.weeks[0] : errors.weeks}
          disabled={isDisabled}
        />

        {/* Streaming Indicator */}
        {isStreaming && (
          <div className="flex items-center space-x-2 text-blue-600">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium">
              Processing your request...
            </span>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isDisabled}
          className={`
            w-full py-3 px-6 rounded-lg font-semibold text-white transition-all duration-200
            ${
              isDisabled
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 focus:ring-2 cursor-pointer focus:ring-blue-500 focus:ring-offset-2"
            }
          `}
        >
          {loading || isSubmitting ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Processing...</span>
            </div>
          ) : (
            "Send Message"
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInputForm;
