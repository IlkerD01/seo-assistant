import React, { useState } from "react";

interface Tab {
  label: string;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
}

export default function Tabs({ tabs }: TabsProps) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div>
      <div style={{ display: "flex", borderBottom: "2px solid #ccc" }}>
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            style={{
              padding: "10px 20px",
              borderBottom: activeTab === index ? "2px solid black" : "none",
              background: "none",
              border: "none",
              cursor: "pointer",
              fontWeight: activeTab === index ? "bold" : "normal",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div style={{ padding: "20px" }}>{tabs[activeTab].content}</div>
    </div>
  );
}