import Layout from "@/components/Layout";

export default function Success() {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen px-4">
        <h1 className="text-4xl font-bold mb-4 text-center">Payment Successful! 🎉</h1>
        <p className="text-lg text-center">
          Thank you for your purchase. You now have access to all premium features.
        </p>
      </div>
    </Layout>
  );
}
