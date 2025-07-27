import React from "react";
import { AuthProvider, useAuth } from "./context/auth-context";
import { Toaster } from "react-hot-toast";
import Login from "./components/login";
import Dashboard from "./components/dashboard";

const AppContent = () => {
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
      {user ? <Dashboard /> : <Login />}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
      <Toaster position="top-center" />
    </AuthProvider>
  );
}

export default App;
