// components/UploadPDF.tsx
import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { pdfUploadSchema, type PDFUploadType } from "../lib/schemas";
import { uploadPDF } from "../lib/api-client";
import { toast } from "react-hot-toast";

// TODO: Add a size limit for the PDF files if needed
const UploadPDF: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<PDFUploadType>({
    resolver: zodResolver(pdfUploadSchema),
  });

  const onSubmit = async (data: PDFUploadType) => {
    const formData = new FormData();
    formData.append("work", data.work[0]);
    formData.append("personal", data.personal[0]);
    formData.append("reflections", data.reflections[0]);
    formData.append("health", data.health[0]);

    try {
      await uploadPDF(formData);
      toast.success("PDFs uploaded successfully!");
      reset(); // Reset the form after successful upload
    } catch (error) {
      console.error("Error uploading PDFs:", error);
      toast.error("Failed to upload PDFs. Please try again.");
    }
  };

  return (
    <div className="p-4 border rounded-md shadow-md max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4">Upload PDF Documents</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <label
          htmlFor="files"
          className="block text-sm font-medium text-gray-700"
        >
          Upload work goals (PDF File) here
        </label>
        <input
          type="file"
          accept="application/pdf"
          {...register("work")}
          className="block w-full text-sm text-gray-700"
        />
        {typeof errors.work?.message === "string" && (
          <p className="text-red-600 text-sm">{errors.work.message}</p>
        )}

        <label
          htmlFor="files"
          className="block text-sm font-medium text-gray-700"
        >
          Upload health and exercise goals (PDF File) here
        </label>
        <input
          type="file"
          accept="application/pdf"
          {...register("personal")}
          className="block w-full text-sm text-gray-700"
        />
        {typeof errors.personal?.message === "string" && (
          <p className="text-red-600 text-sm">{errors.personal.message}</p>
        )}

        <label
          htmlFor="files"
          className="block text-sm font-medium text-gray-700"
        >
          Upload house related chores (PDF File) here
        </label>
        <input
          type="file"
          accept="application/pdf"
          {...register("reflections")}
          className="block w-full text-sm text-gray-700"
        />
        {typeof errors.reflections?.message === "string" && (
          <p className="text-red-600 text-sm">{errors.reflections.message}</p>
        )}

        <label
          htmlFor="files"
          className="block text-sm font-medium text-gray-700"
        >
          Upload health related documents (PDF File) here
        </label>
        <input
          type="file"
          accept="application/pdf"
          {...register("health")}
          className="block w-full text-sm text-gray-700"
        />
        {typeof errors.health?.message === "string" && (
          <p className="text-red-600 text-sm">{errors.health.message}</p>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? "Uploading..." : "Upload PDFs"}
        </button>
      </form>
    </div>
  );
};

export default UploadPDF;
