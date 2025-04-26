import { useState } from "react";

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
    <div>
      <h1>Checkout Pagina</h1>
      <button onClick={createCheckoutSession} disabled={loading}>
        {loading ? "Even geduld..." : "Start Checkout"}
      </button>
    </div>
  );
}
