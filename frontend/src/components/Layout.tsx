import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header style={{ backgroundColor: "#f8f9fa", padding: "1rem", borderBottom: "1px solid #dee2e6" }}>
        <h1 style={{ margin: 0, fontSize: "24px", textAlign: "center" }}>SEO Assistant</h1>
      </header>

      <main style={{ flex: 1, padding: "2rem", maxWidth: "1000px", margin: "0 auto" }}>
        {children}
      </main>

      <footer style={{ backgroundColor: "#f8f9fa", padding: "1rem", borderTop: "1px solid #dee2e6", textAlign: "center" }}>
        <small>© {new Date().getFullYear()} SEO Assistant. Alle rechten voorbehouden.</small>
      </footer>
    </div>
  );
}
