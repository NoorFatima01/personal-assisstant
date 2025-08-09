// components/WeekSelector.tsx
import React from "react";
import { type UseFormSetValue, type FieldError } from "react-hook-form";
import { type ChatInputFormData } from "../lib/types";
import { handleWeekChange } from "../utils/chat-utils";

interface WeekSelectorProps {
  weeks: string[];
  selectedWeeks: string[];
  setValue: UseFormSetValue<ChatInputFormData>;
  error?: FieldError;
  disabled?: boolean;
}

const WeekSelector: React.FC<WeekSelectorProps> = ({
  weeks,
  selectedWeeks,
  setValue,
  error,
  disabled = false,
}) => {
  return (
    <div className="space-y-3">
      <label className="block text-sm font-semibold text-gray-700">
        Select Weeks to Analyze
        {selectedWeeks.length > 0 && (
          <span className="ml-2 text-xs text-blue-600 font-normal">
            ({selectedWeeks.length} selected)
          </span>
        )}
      </label>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {weeks.map((week) => {
          const isSelected = selectedWeeks.includes(week);
          return (
            <label
              key={week}
              className={`
                flex items-center space-x-3 p-3 rounded-lg border-2 cursor-pointer transition-all duration-200
                ${
                  isSelected
                    ? "border-blue-500 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                }
                ${disabled ? "opacity-50 cursor-not-allowed" : ""}
              `}
            >
              <input
                type="checkbox"
                checked={isSelected}
                onChange={(e) =>
                  handleWeekChange(
                    week,
                    e.target.checked,
                    selectedWeeks,
                    setValue
                  )
                }
                disabled={disabled}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
              />
              <span className="text-sm font-medium select-none">{week}</span>
            </label>
          );
        })}
      </div>

      {selectedWeeks.length > 0 && (
        <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-700 font-medium mb-1">
            Selected weeks:
          </p>
          <p className="text-sm text-blue-600">{selectedWeeks.join(", ")}</p>
        </div>
      )}

      {error && (
        <p className="text-red-500 text-sm mt-1 flex items-center">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
          {error.message}
        </p>
      )}
    </div>
  );
};

export default WeekSelector;
