import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { chatInputFormSchema, type ChatInputFormType } from "../lib/schemas";
import { validateChatInput } from "../utils/chat-utils";
import { handleWeekChange } from "../utils/chat-utils";

type ChatInputFormProps = {
  weeks: string[];
  loading: boolean;
  onSend: (input: string, weeks: string[]) => void;
  isStreaming: boolean;
};

const ChatInputForm = ({
  weeks,
  loading,
  onSend,
  isStreaming,
}: ChatInputFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    setValue,
    watch,
  } = useForm<ChatInputFormType>({
    resolver: zodResolver(chatInputFormSchema),
    defaultValues: {
      weeks: [],
    },
  });

  const selectedWeeks = watch("weeks") || [];

  const onSubmit = (data: ChatInputFormType) => {
    if (!validateChatInput(data)) return;
    const sortedWeeks = [...data.weeks].sort(
      (a, b) => new Date(b).getTime() - new Date(a).getTime()
    );
    onSend(data.question, sortedWeeks);
    reset();
  };

  console.log("Weeks are: ", weeks);

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Question Input */}
        <div>
          <input
            className="w-full border rounded px-3 py-2"
            placeholder="Ask me anything..."
            {...register("question")}
            disabled={loading}
          />
          {errors.question && (
            <p className="text-red-500 text-sm mt-1">
              {errors.question.message}
            </p>
          )}
        </div>

        {/* Week Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Select Weeks:
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
            {weeks.map((week) => (
              <label
                key={week}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedWeeks.includes(week)}
                  onChange={(e) =>
                    handleWeekChange(
                      week,
                      e.target.checked,
                      selectedWeeks,
                      setValue
                    )
                  }
                  disabled={loading}
                  className="rounded"
                />
                <span className="text-sm">{week}</span>
              </label>
            ))}
          </div>
          {errors.weeks && (
            <p className="text-red-500 text-sm mt-1">{errors.weeks.message}</p>
          )}
        </div>

        {/* Selected weeks display */}
        {selectedWeeks.length > 0 && (
          <div className="text-sm text-gray-600">
            Selected: {selectedWeeks.join(", ")}
          </div>
        )}
        {isStreaming && <span className="animate-pulse">...</span>}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || isSubmitting}
          className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded"
        >
          {loading || isSubmitting ? "Submitting..." : "Submit"}
        </button>
      </form>
    </div>
  );
};

export default ChatInputForm;
