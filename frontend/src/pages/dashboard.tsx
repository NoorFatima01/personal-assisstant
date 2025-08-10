import { useAuth } from "../context/auth-context";
import MyChats from "../components/my-chats";
import Loader from "../components/loader";
import DashboardHeader from "../components/dashboard-header";
import WelcomeSection from "../components/welcome-section";
import ActionCard from "../components/action-card";
import { useEffect } from "react";

const Dashboard = () => {
  useEffect(() => {
    window.document.title = "Chat Week Plan | Dashboard";
  }, []);

  const { user } = useAuth();

  if (!user) {
    return <Loader />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <DashboardHeader email={user?.email} />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Tips Section */}
        <WelcomeSection />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions Card */}
          <div className="lg:col-span-1">
            <ActionCard />
          </div>

          {/* Chat History Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Recent Conversations
                </h3>
              </div>
              <MyChats userId={user?.id} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
