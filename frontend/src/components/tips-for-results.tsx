const TipsForResults = () => {
  return (
    <div className="mt-8 bg-blue-50 rounded-lg p-6 border border-blue-200">
      <div className="flex items-start gap-4">
        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
          <svg
            className="w-4 h-4 text-blue-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">
            Tips for better results
          </h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• Upload PDF files only for best compatibility</li>
            <li>• Include clear, readable text for better analysis</li>
            <li>
              • All uploads are necessary - share what's comfortable for you
            </li>
            <li>• Your documents are processed securely and privately</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TipsForResults;
