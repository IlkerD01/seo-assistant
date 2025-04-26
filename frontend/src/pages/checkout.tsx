import { useState } from "react";
import Layout from "@/components/Layout";
import Spinner from "@/components/ui/Spinner";

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
        window.location.href = session.url;
      } else {
        alert("Error creating checkout session.");
        setLoading(false);
      }
    } catch (error) {
      console.error("Checkout error:", error);
      alert("Error connecting to server.");
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen px-4">
        <h1 className="text-4xl font-bold mb-4 text-center">Checkout</h1>
        <p className="text-lg mb-8 text-center">
          Secure your access to premium SEO tools in just a few clicks.
        </p>
        {loading ? (
          <Spinner />
        ) : (
          <button
            onClick={createCheckoutSession}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-md text-lg transition"
          >
            Proceed to Payment
          </button>
        )}
      </div>
    </Layout>
  );
}
