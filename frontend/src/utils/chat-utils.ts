import { toast } from "react-hot-toast/headless";
import type { ChatInputFormType } from "../lib/schemas";
import type { UseFormSetValue } from "react-hook-form";


export const handleWeekChange = (
  week: string,
  checked: boolean,
  selectedWeeks: string[],
  setValue: UseFormSetValue<{ question: string; weeks: string[] }>
) => {
  let updatedWeeks;
  if (checked) {
    updatedWeeks = [...selectedWeeks, week];
  } else {
    updatedWeeks = selectedWeeks.filter((w) => w !== week);
  }
  setValue("weeks", updatedWeeks);
};

export const validateChatInput = (data: ChatInputFormType) => {
  if (!data.question.trim()) {
    toast.error("Question cannot be empty");
    return false;
  }
  if (data.weeks.length === 0) {
    toast.error("Please select at least one week");
    return false;
  }
  return true;
};


