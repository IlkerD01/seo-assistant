import Head from 'next/head';
import "@/styles/globals.css";
import type { AppProps } from "next/app";
<Head>
  <title>SEO Assistant - Boost Your SEO</title>
  <meta name="description" content="Unlock premium SEO tools with SEO Assistant." />
</Head>



export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
