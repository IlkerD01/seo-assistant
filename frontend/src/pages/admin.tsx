import Tabs from "../components/ui/tabs";

export default function Admin() {
  const tabs = [
    { label: "API Keys", content: <div>Hier kan je API sleutels beheren.</div> },
    { label: "Gebruikers", content: <div>Hier kan je gebruikers beheren.</div> },
  ];

  return (
    <div style={{ padding: 20 }}>
      <h1>Admin Dashboard</h1>
      <Tabs tabs={tabs} />
    </div>
  );
}
