import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to SEO Assistant</h1>
      <Link href="/checkout">
        <button style={{ marginTop: '20px' }}>Buy Now</button>
      </Link>
    </div>
  );
}
