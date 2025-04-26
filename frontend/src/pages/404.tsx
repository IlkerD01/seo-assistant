import Layout from "@/components/Layout";
import { useRouter } from "next/router";

export default function NotFound() {
  const router = useRouter();

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen px-4 text-center">
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <h2 className="text-2xl font-semibold mb-4">Page Not Found</h2>
        <p className="text-lg mb-8">
          Sorry, the page you're looking for doesn't exist.
        </p>
        <button
          onClick={() => router.push("/")}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-lg transition"
        >
          Return Home
        </button>
      </div>
    </Layout>
  );
}
