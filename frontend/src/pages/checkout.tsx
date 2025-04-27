import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';

export default function Checkout() {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/create-checkout-session', {
      method: 'POST',
    });
    const session = await response.json();

    if (session.id) {
      const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!);
      
      if (!stripe) {
        alert('Stripe could not be loaded.');
        setLoading(false);
        return;
      }

      await stripe.redirectToCheckout({ sessionId: session.id });
    } else {
      alert('Checkout error');
    }
    setLoading(false);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Checkout</h1>
      <button onClick={handleCheckout} disabled={loading}>
        {loading ? 'Loading...' : 'Proceed to Payment'}
      </button>
    </div>
  );
}
