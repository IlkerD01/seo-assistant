import Layout from "@/components/Layout";

export default function Cancelled() {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen px-4">
        <h1 className="text-4xl font-bold mb-4 text-center">Payment Cancelled ❌</h1>
        <p className="text-lg text-center">
          Your payment was cancelled. Feel free to try again when you're ready.
        </p>
      </div>
    </Layout>
  );
}
