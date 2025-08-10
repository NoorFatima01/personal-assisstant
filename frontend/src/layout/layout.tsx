import React from "react";
import { useAuth } from "../context/auth-context";
import { Link } from "react-router";
import logo from "../assets/plan.png";

const Layout = ({ children }: { children: React.ReactNode }) => {
  const { user, signOut } = useAuth();

  const handleSignOut = async () => {
    await signOut();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo/Brand */}
            <div className="flex-shrink-0">
              <Link to="/" className="text-xl font-semibold text-gray-900 flex items-center">
                <img src={logo} alt="Logo" className="h-8" />
                <span className="ml-2">Week Plan Chat</span>
              </Link>
            </div>

            {/* User Info & Sign Out */}
            {user && (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">{user.email}</span>
                <button
                  onClick={handleSignOut}
                  className="bg-red-600 hover:bg-red-700 cursor-pointer text-white px-3 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
                >
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">{children}</div>
      </main>
    </div>
  );
};

export default Layout;
