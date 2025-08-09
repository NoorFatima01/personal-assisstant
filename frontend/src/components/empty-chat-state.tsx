import React from "react";

const EmptyChatState: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center space-y-6 max-w-md mx-auto p-8">
        <div className="w-24 h-24 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
          <svg
            className="w-12 h-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
        </div>
        <div className="space-y-2">
          <h3 className="text-xl font-semibold text-gray-900">
            No Documents Found
          </h3>
          <p className="text-gray-600">
            Looks like you haven't uploaded any documents yet. Please upload
            documents to get started with your AI chat.
          </p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors">
          Upload Documents
        </button>
      </div>
    </div>
  );
};

export default EmptyChatState;
