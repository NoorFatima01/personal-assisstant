import React from "react";

interface StreamingControlsProps {
  isStreaming: boolean;
  onEndStreaming: () => void;
}

const StreamingControls: React.FC<StreamingControlsProps> = ({
  isStreaming,
  onEndStreaming,
}) => {
  if (!isStreaming) return null;

  return (
    <div className="flex justify-center mt-4">
      <button
        onClick={onEndStreaming}
        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
      >
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z"
            clipRule="evenodd"
          />
        </svg>
        <span>Stop Generation</span>
      </button>
    </div>
  );
};

export default StreamingControls;
