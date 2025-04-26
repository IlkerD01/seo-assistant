// src/pages/success.tsx
import Layout from "@/components/Layout";

export default function Success() {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-4xl font-bold mb-4">Bedankt voor je betaling! 🎉</h1>
        <p>Je hebt nu toegang tot de premium API functies.</p>
      </div>
    </Layout>
  );
}
