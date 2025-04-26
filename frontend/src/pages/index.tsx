import Layout from "@/components/Layout";
import { useRouter } from "next/router";
import Image from "next/image";

export default function Home() {
  const router = useRouter();

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-screen px-6 bg-gradient-to-b from-blue-50 to-white">
        <h1 className="text-5xl font-bold text-center mb-4 text-blue-700">Welcome to SEO Assistant 🚀</h1>
        <p className="text-lg text-center mb-6 max-w-2xl">
          Unlock premium SEO tools and boost your website's performance effortlessly with our premium API access.
        </p>

        <div className="w-full max-w-md">
          <Image
            src="/images/seo-illustration.png"
            alt="SEO Tools Illustration"
            width={500}
            height={300}
            priority
            className="rounded-lg shadow-lg"
          />
        </div>

        <button
          onClick={() => router.push("/checkout")}
          className="mt-8 px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition"
        >
          Get Started
        </button>
      </div>
    </Layout>
  );
}
