import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { pdfUploadSchema, type PDFUploadType } from "../lib/schemas";
import { uploadPDF } from "../utils/api-client";
import { toast } from "react-hot-toast";

// TODO: Add a size limit for the PDF files if needed
// TODO: refactor code to prevent repeated code for each file input
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
    formData.append("week_start", data.week_start);

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
    <div>
      {/* Main Form Card */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div className="px-8 py-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            Weekly Document Upload
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            All fields are optional. Upload what's relevant for your week.
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="p-8 space-y-8">
          {/* Week Selection */}
          <div className="space-y-2">
            <label
              htmlFor="week_start"
              className="block text-sm font-medium text-gray-900"
            >
              📅 Week Starting Date
            </label>
            <input
              type="date"
              {...register("week_start")}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900"
            />
            {typeof errors.week_start?.message === "string" && (
              <p className="text-red-500 text-sm flex items-center gap-1">
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                {errors.week_start.message}
              </p>
            )}
          </div>

          {/* File Upload Sections */}
          <div className="grid gap-6">
            {/* Work Goals */}
            <div className="border border-gray-200 rounded-lg p-6 hover:border-blue-300 transition-colors duration-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-blue-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6"
                    />
                  </svg>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900">
                    Work Goals
                  </label>
                  <p className="text-xs text-gray-500">
                    Upload your professional objectives and targets
                  </p>
                </div>
              </div>
              <input
                type="file"
                accept="application/pdf"
                {...register("work")}
                className="w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 file:cursor-pointer cursor-pointer"
              />
              {typeof errors.work?.message === "string" && (
                <p className="text-red-500 text-sm flex items-center gap-1 mt-2">
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  {errors.work.message}
                </p>
              )}
            </div>

            {/* Personal Goals */}
            <div className="border border-gray-200 rounded-lg p-6 hover:border-green-300 transition-colors duration-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900">
                    Personal Goals
                  </label>
                  <p className="text-xs text-gray-500">
                    Share your personal development objectives
                  </p>
                </div>
              </div>
              <input
                type="file"
                accept="application/pdf"
                {...register("personal")}
                className="w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-green-50 file:text-green-700 hover:file:bg-green-100 file:cursor-pointer cursor-pointer"
              />
              {typeof errors.personal?.message === "string" && (
                <p className="text-red-500 text-sm flex items-center gap-1 mt-2">
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  {errors.personal.message}
                </p>
              )}
            </div>

            {/* Reflections */}
            <div className="border border-gray-200 rounded-lg p-6 hover:border-purple-300 transition-colors duration-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-purple-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900">
                    Reflections
                  </label>
                  <p className="text-xs text-gray-500">
                    Upload your thoughts and insights from the week
                  </p>
                </div>
              </div>
              <input
                type="file"
                accept="application/pdf"
                {...register("reflections")}
                className="w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 file:cursor-pointer cursor-pointer"
              />
              {typeof errors.reflections?.message === "string" && (
                <p className="text-red-500 text-sm flex items-center gap-1 mt-2">
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  {errors.reflections.message}
                </p>
              )}
            </div>

            {/* Health Documents */}
            <div className="border border-gray-200 rounded-lg p-6 hover:border-red-300 transition-colors duration-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-red-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                    />
                  </svg>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-900">
                    Health Documents
                  </label>
                  <p className="text-xs text-gray-500">
                    Upload wellness reports, fitness logs, or health goals
                  </p>
                </div>
              </div>
              <input
                type="file"
                accept="application/pdf"
                {...register("health")}
                className="w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-red-50 file:text-red-700 hover:file:bg-red-100 file:cursor-pointer cursor-pointer"
              />
              {typeof errors.health?.message === "string" && (
                <p className="text-red-500 text-sm flex items-center gap-1 mt-2">
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  {errors.health.message}
                </p>
              )}
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-6 border-t border-gray-200">
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium py-4 px-6 rounded-lg transition-all duration-200 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed shadow-lg hover:shadow-xl disabled:shadow-none"
            >
              {isSubmitting ? (
                <div className="flex items-center justify-center gap-3">
                  <svg
                    className="animate-spin w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"
                    />
                  </svg>
                  <span>Uploading your documents...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center cursor-pointer gap-3">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                  <span>Upload Documents</span>
                </div>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadPDF;
