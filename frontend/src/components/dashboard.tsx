import { useAuth } from "../context/auth-context";
import { Link, useNavigate } from "react-router";
import { v4 as uuidv4 } from 'uuid';

const Dashboard = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
  };

  const startNewChat = () => {
    // Generate a new chat session ID
    const chatId = uuidv4();
    navigate(`/chat/${chatId}`);
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Welcome!</h2>
      <p className="mb-4">Email: {user?.email || "No email"}</p>
      <p className="mb-6">User ID: {user?.id}</p>

      <button
        onClick={handleSignOut}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        Sign Out
      </button>
      <Link to="/upload-docs" className="mt-4 inline-block text-blue-600 hover:underline">
        Upload Documents
      </Link>
      <button onClick={startNewChat} className="mt-4 inline-block text-blue-600 hover:underline">
        Chat with Assistant
      </button>
    </div>
  );
};

export default Dashboard;