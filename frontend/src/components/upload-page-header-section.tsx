import React from "react";

const UploadHeader = () => {
  return (
    <div className="text-center mb-8">
      <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
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
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
      </div>
      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        Upload Your Documents
      </h1>
      <p className="text-gray-600">
        Upload your weekly goals and reflections to get personalized insights
      </p>
    </div>
  );
};

export default UploadHeader;
