import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import Tabs from "@/components/ui/Tabs";

export default function Admin() {
  const [selectedTab, setSelectedTab] = useState<string>("API Keys");
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  const logout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  const tabs = [
    { label: "API Keys", content: <p>Manage and generate API keys for your users here.</p> },
    { label: "Users", content: <p>View and manage users registered to your platform.</p> },
    { label: "Settings", content: <p>Adjust your platform settings here.</p> },
  ];

  if (!isAuthenticated) {
    return null; // Wait until auth is checked
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto p-4 flex flex-col items-center min-h-screen">
        <div className="flex justify-between items-center w-full mb-6">
          <h1 className="text-4xl font-bold text-center flex-1">Admin Dashboard</h1>
          <button
            onClick={logout}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md text-sm transition ml-4"
          >
            Logout
          </button>
        </div>

        <Tabs tabs={tabs} selectedTab={selectedTab} setSelectedTab={setSelectedTab} />

        <div className="mt-8 w-full">
          {tabs.map((tab) =>
            tab.label === selectedTab ? (
              <div key={tab.label} className="text-center text-lg">
                {tab.content}
              </div>
            ) : null
          )}
        </div>
      </div>
    </Layout>
  );
}
