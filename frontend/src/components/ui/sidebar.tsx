import React from "react";

interface SidebarProps {
  items: { label: string; onClick: () => void }[];
}

export default function Sidebar({ items }: SidebarProps) {
  return (
    <div style={styles.sidebar}>
      {items.map((item, index) => (
        <button
          key={index}
          onClick={item.onClick}
          style={styles.sidebarButton}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}

const styles = {
  sidebar: {
    width: "200px",
    backgroundColor: "#f5f5f5",
    padding: "1rem",
    height: "100vh",
    position: "fixed" as "fixed",
    top: 0,
    left: 0,
    display: "flex",
    flexDirection: "column" as "column",
    gap: "1rem",
    borderRight: "1px solid #ddd",
  },
  sidebarButton: {
    background: "none",
    border: "none",
    textAlign: "left" as "left",
    fontSize: "16px",
    color: "#333",
    cursor: "pointer",
  },
};
