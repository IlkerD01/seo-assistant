import { useState } from "react";
import Layout from "@/components/Layout";
import Spinner from "@/components/ui/spinner";

export default function Checkout() {
  const [loading, setLoading] = useState(false);

  const createCheckoutSession = async () => {
    setLoading(true);
    try {
      const response = await fetch("https://seo-assistant-r44h.onrender.com/create-checkout-session", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const session = await response.json();

      if (session && session.url) {
        window.location.href = session.url; // Stripe redirect
      } else {
        alert("Fout bij het aanmaken van een checkout sessie.");
        setLoading(false);
      }
    } catch (error) {
      console.error("Fout bij starten checkout:", error);
      alert("Fout bij verbinding met server.");
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h1 style={{ textAlign: "center", marginBottom: "2rem" }}>Checkout Pagina</h1>
      <div style={{ textAlign: "center" }}>
        <button 
          onClick={createCheckoutSession} 
          disabled={loading}
          style={{
            backgroundColor: "#0070f3",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          {loading ? <Spinner /> : "Start Checkout"}
        </button>
      </div>
    </Layout>
  );
}

