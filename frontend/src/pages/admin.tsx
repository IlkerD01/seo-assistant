import Tabs from "@/components/ui/tabs";

export default function Admin() {
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
    <div style={pageStyles.container}>
      <h1 style={pageStyles.title}>Admin Dashboard</h1>
      <Tabs tabs={tabs} />
    </div>
  );
}

const pageStyles = {
  container: {
    maxWidth: "900px",
    margin: "0 auto",
    padding: "2rem",
  },
  title: {
    textAlign: "center" as "center",
    marginBottom: "2rem",
    fontSize: "2rem",
    color: "#333",
  },
};
