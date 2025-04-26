import React from "react";

interface TabsProps {
  tabs: { label: string; content: React.ReactNode }[];
  selectedTab: string;
  setSelectedTab: (tab: string) => void;
}

export default function Tabs({ tabs, selectedTab, setSelectedTab }: TabsProps) {
  return (
    <div className="flex flex-col">
      <div className="flex space-x-4 border-b pb-2">
        {tabs.map((tab) => (
          <button
            key={tab.label}
            onClick={() => setSelectedTab(tab.label)}
            className={`px-4 py-2 rounded-t ${
              selectedTab === tab.label
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="mt-4">
        {tabs.find((tab) => tab.label === selectedTab)?.content}
      </div>
    </div>
  );
}

