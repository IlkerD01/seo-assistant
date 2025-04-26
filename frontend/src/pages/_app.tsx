import Head from 'next/head';
import "@/styles/globals.css";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>SEO Assistant - Boost Your SEO</title>
        <meta name="description" content="Unlock premium SEO tools with SEO Assistant." />
      </Head>
      <Component {...pageProps} />
    </>
  );
}
