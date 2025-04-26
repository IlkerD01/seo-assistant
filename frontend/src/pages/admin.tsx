import { useState } from "react";
import Layout from "@/components/Layout";
import Tabs from "@/components/ui/Tabs";

export default function Admin() {
  const [selectedTab, setSelectedTab] = useState<string>("API Keys");

  const tabs = [
    { label: "API Keys", content: <p>Manage and generate API keys for your users here.</p> },
    { label: "Users", content: <p>View and manage users registered to your platform.</p> },
    { label: "Settings", content: <p>Adjust your platform settings here.</p> },
  ];

  return (
    <Layout>
      <div className="max-w-4xl mx-auto p-4 flex flex-col items-center min-h-screen">
        <h1 className="text-4xl font-bold mb-8 text-center">Admin Dashboard</h1>

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
