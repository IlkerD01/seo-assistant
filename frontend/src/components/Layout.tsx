import React, { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div style={{ 
      maxWidth: "900px", 
      margin: "0 auto", 
      padding: "2rem", 
      fontFamily: "Arial, sans-serif" 
    }}>
      {children}
    </div>
  );
};

export default Layout;
