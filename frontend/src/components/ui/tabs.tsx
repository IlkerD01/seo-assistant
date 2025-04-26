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
      <div style={styles.tabList}>
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            style={{
              ...styles.tabButton,
              ...(activeTab === index ? styles.activeTabButton : {}),
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div style={styles.tabContent}>
        {tabs[activeTab].content}
      </div>
    </div>
  );
}

const styles = {
  tabList: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "1rem",
    borderBottom: "2px solid #ccc",
  },
  tabButton: {
    padding: "10px 20px",
    margin: "0 5px",
    background: "none",
    border: "none",
    borderBottom: "2px solid transparent",
    cursor: "pointer",
    fontWeight: "bold" as "bold",
    fontSize: "16px",
    color: "#333",
  },
  activeTabButton: {
    borderBottom: "2px solid #0070f3",
    color: "#0070f3",
  },
  tabContent: {
    padding: "20px",
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    minHeight: "200px",
  },
};
