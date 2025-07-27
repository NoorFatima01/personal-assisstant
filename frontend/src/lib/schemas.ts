import { z } from "zod";

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.email(),
  created_at: z.iso.datetime(),
  updated_at: z.iso.datetime(),
});
export type UserType = z.infer<typeof UserSchema>;

export const pdfUploadSchema = z.object({
  work: z
    .any()
    .refine(
      (file: File) => file && file.size > 0,
      "You must upload at least one PDF file."
    )
    .refine(
      (file: File) => file.type === "application/pdf",
      "All files must be PDFs."
    ),
  personal: z
    .any()
    .refine(
      (file: File) => file && file.size > 0,
      "You must upload at least one PDF file."
    )
    .refine(
      (file: File) => file.type === "application/pdf",
      "All files must be PDFs."
    ),
  reflections: z
    .any()
    .refine(
      (file: File) => file && file.size > 0,
      "You must upload at least one PDF file."
    )
    .refine(
      (file: File) => file.type === "application/pdf",
      "All files must be PDFs."
    ),
  health: z
    .any()
    .refine(
      (file: File) => file && file.size > 0,
      "You must upload at least one PDF file."
    )
    .refine(
      (file: File) => file.type === "application/pdf",
      "All files must be PDFs."
    ),
});

export type PDFUploadType = z.infer<typeof pdfUploadSchema>;
