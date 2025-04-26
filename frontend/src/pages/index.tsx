import Layout from "@/components/Layout";
import { useRouter } from "next/router";
import Image from "next/image";

export default function Home() {
  const router = useRouter();

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen px-6">
        <h1 className="text-4xl font-bold mb-4 text-center">
          Welcome to SEO Assistant 🚀
        </h1>

        <div className="flex justify-center mt-6">
          <Image 
            src="/images/seo-illustration.png" 
            alt="SEO Tools Illustration" 
            width={500} 
            height={300} 
            priority
          />
        </div>

        <p className="text-lg text-center mt-6 mb-8 max-w-2xl">
          Unlock premium API features and boost your SEO performance effortlessly.
        </p>

        <button
          onClick={() => router.push("/checkout")}
          className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg text-lg transition"
        >
          Start Checkout
        </button>
      </div>
    </Layout>
  );
}
