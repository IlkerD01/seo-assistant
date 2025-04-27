import { useState } from 'react';

export default function Checkout() {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/create-checkout-session', {
      method: 'POST',
    });
    const session = await response.json();

    if (session.id) {
  const stripePromise = (await import('@stripe/stripe-js')).loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!);
  const stripe = await stripePromise;

  if (!stripe) {
    alert('Stripe kon niet geladen worden');
    return;
  }

  await stripe.redirectToCheckout({ sessionId: session.id });
} else {
  alert('Checkout error');
}if (session.id) {
  const stripePromise = (await import('@stripe/stripe-js')).loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!);
  const stripe = await stripePromise;

  if (!stripe) {
    alert('Stripe kon niet geladen worden');
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
