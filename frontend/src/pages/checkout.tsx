import { useState } from "react";

export default function Checkout() {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/create-checkout-session", {
      method: "POST",
    });
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Checkout Pagina</h1>
      <button onClick={handleCheckout} disabled={loading}>
        {loading ? "Even geduld..." : "Betaal nu"}
      </button>
    </div>
  );
}