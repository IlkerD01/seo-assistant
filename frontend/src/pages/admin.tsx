import { useState } from "react";
import Tabs from "@/components/ui/tabs";

export default function Admin() {
  const [selectedTab, setSelectedTab] = useState<string>("API Key's");

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

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
      <h1 style={{ textAlign: "center", marginBottom: "2rem" }}>Admin Dashboard</h1>

      <Tabs tabs={tabs} />

      {/* Eventueel extra inhoud */}
      <div style={{ marginTop: "2rem" }}>
        {/* Als je extra content wil tonen afhankelijk van geselecteerde tab, kan je dat hier toevoegen */}
      </div>
    </div>
  );
}

