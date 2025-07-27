import React from "react";
import { useAuth } from "../context/auth-context";

const Dashboard = () => {
  const { user, signOut } = useAuth();

  const handleSignOut = async () => {
    await signOut();
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Welcome!</h2>
      <p className="mb-4">Email: {user?.email || "No email"}</p>
      <p className="mb-6">User ID: {user?.id}</p>

      <button
        onClick={handleSignOut}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        Sign Out
      </button>
    </div>
  );
};

export default Dashboard;
