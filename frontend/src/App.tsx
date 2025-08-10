import React from "react";
import { AuthProvider, useAuth } from "./context/auth-context";
import { BrowserRouter } from "react-router-dom";
import { Route, Routes, Navigate } from "react-router";
import { Toaster } from "react-hot-toast";
import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import UploadDocPage from "./pages/upload-doc-page";
import Chat from "./pages/chat";
import Layout from "./layout/layout";
import Loader from "./components/loader";

const ProtectedRoute: React.FC<{ element: React.ReactElement }> = ({
  element,
}) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {user ? <Layout>{element}</Layout> : <Navigate to="/login" replace />}
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
