import React from "react";
import { AuthProvider, useAuth } from "./context/auth-context";
import { BrowserRouter } from "react-router-dom";
import { Route, Routes, Navigate } from "react-router";
import { Toaster } from "react-hot-toast";
import Login from "./components/login";
import Dashboard from "./components/dashboard";
import UploadDocPage from "./pages/upload-doc-page";
import Chat from "./pages/chat";

const ProtectedRoute: React.FC<{ element: React.ReactElement }> = ({
  element,
}) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {user ? element : <Navigate to="/login" replace />}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={<ProtectedRoute element={<Dashboard />} />}
          />
          <Route path="/login" element={<Login />} />
          <Route
            path="/upload-docs"
            element={<ProtectedRoute element={<UploadDocPage />} />}
          />
          <Route
            path="/chat/:chatId"
            element={<ProtectedRoute element={<Chat />} />}
          />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </AuthProvider>
  );
}

export default App;
