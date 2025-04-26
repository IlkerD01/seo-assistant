import { useState } from "react";
import Tabs from "@/components/ui/tabs";
import Sidebar from "@/components/ui/sidebar";

export default function Admin() {
  const [selectedTab, setSelectedTab] = useState(0);

  const tabs = [
    { 
      label: "API Key's",
      content: (
        <div>
          <h2>Beheer API Keys</h2>
          <p>Hier kan je nieuwe API keys aanmaken en verwijderen.</p>
        </div>
      ),
    },
    { 
      label: "Gebruikers",
      content: (
        <div>
          <h2>Gebruikers Overzicht</h2>
          <p>Hier zie je alle gebruikers van je platform.</p>
        </div>
      ),
    },
    { 
      label: "Instellingen",
      content: (
        <div>
          <h2>Instellingen</h2>
          <p>Hier kan je admin-instellingen aanpassen.</p>
        </div>
      ),
    },
  ];

  const sidebarItems = tabs.map((tab, index) => ({
    label: tab.label,
    onClick: () => setSelectedTab(index),
  }));

  return (
    <div style={pageStyles.container}>
      <Sidebar items={sidebarItems} />
      <div style={pageStyles.content}>
        <h1 style={pageStyles.title}>Admin Dashboard</h1>
        <Tabs tabs={tabs} />
      </div>
    </div>
  );
}

const pageStyles = {
  container: {
    display: "flex",
  },
  content: {
    marginLeft: "220px",
    padding: "2rem",
    width: "100%",
  },
  title: {
    textAlign: "center" as "center",
    marginBottom: "2rem",
    fontSize: "2rem",
    color: "#333",
  },
};

