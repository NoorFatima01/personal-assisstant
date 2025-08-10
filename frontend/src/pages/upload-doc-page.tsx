import UploadPDF from "../form/upload-pdf-form";
import UploadHeader from "../components/upload-page-header-section";
import TipsForResults from "../components/tips-for-results";
import { useEffect } from "react";

const UploadDocPage = () => {
  useEffect(() => {
    window.document.title = "Upload | Week Plan Chat";
  }, []);
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header Section */}
        <UploadHeader />
        {/* PDF Upload Section */}
        <UploadPDF />
        {/* Help Section */}
        <TipsForResults />
      </div>
    </div>
  );
};

export default UploadDocPage;
