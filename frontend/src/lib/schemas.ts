import {  z } from "zod";

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.email(),
  created_at: z.iso.datetime(),
  updated_at: z.iso.datetime(),
});
export type UserType = z.infer<typeof UserSchema>;

export const pdfUploadSchema = z.object({
  week_start: z
    .string()
    .min(1, "Week start date is required")
    .refine(
      (dateString) => !isNaN(Date.parse(dateString)),
      "Invalid date format. Please provide a valid date."
    ),
  work: z
    .any()
    .refine(
      (files: FileList) => files && files.length > 0 && files[0].size > 0,
      "You must upload a work PDF file."
    )
    .refine(
      (files: FileList) =>
        files && files[0] && files[0].type === "application/pdf",
      "Work file must be a PDF."
    ),
  personal: z
    .any()
    .refine(
      (files: FileList) => files && files.length > 0 && files[0].size > 0,
      "You must upload a personal PDF file."
    )
    .refine(
      (files: FileList) =>
        files && files[0] && files[0].type === "application/pdf",
      "Personal file must be a PDF."
    ),
  reflections: z
    .any()
    .refine(
      (files: FileList) => files && files.length > 0 && files[0].size > 0,
      "You must upload a reflections PDF file."
    )
    .refine(
      (files: FileList) =>
        files && files[0] && files[0].type === "application/pdf",
      "Reflections file must be a PDF."
    ),
  health: z
    .any()
    .refine(
      (files: FileList) => files && files.length > 0 && files[0].size > 0,
      "You must upload a health PDF file."
    )
    .refine(
      (files: FileList) =>
        files && files[0] && files[0].type === "application/pdf",
      "Health file must be a PDF."
    ),
});
export type PDFUploadType = z.infer<typeof pdfUploadSchema>;


export const chatInputFormSchema = z.object({
  question: z.string().min(1, "Question is required"),
  weeks: z.array(z.string()).min(1, "At least one week must be selected"),
});
export type ChatInputFormType = z.infer<typeof chatInputFormSchema>;
