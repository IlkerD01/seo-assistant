// src/pages/checkout.tsx
import { useState } from "react";
import Layout from "@/components/Layout";
import Spinner from "@/components/ui/Spinner";

export default function Checkout() {
  const [loading, setLoading] = useState(false);

  const startCheckout = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/create-checkout-session", {
        method: "POST",
      });
      const data = await response.json();
      if (data.url) {
        window.location.href = data.url;
      } else {
        alert("Fout bij het starten van checkout.");
        setLoading(false);
      }
    } catch (error) {
      console.error("Checkout error:", error);
      alert("Er ging iets fout.");
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-3xl font-bold mb-6">Checkout Pagina</h1>
        <button
          onClick={startCheckout}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md shadow-md disabled:opacity-50"
          disabled={loading}
        >
          {loading ? <Spinner /> : "Start Checkout"}
        </button>
      </div>
    </Layout>
  );
}



