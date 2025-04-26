import React from "react";

interface SpinnerProps {
  message?: string;
}

export default function Spinner({ message = "Even geduld..." }: SpinnerProps) {
  return (
    <div style={styles.overlay}>
      <div style={styles.spinner}></div>
      <p style={styles.message}>{message}</p>
    </div>
  );
}

const styles = {
  overlay: {
    display: "flex",
    flexDirection: "column" as "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "rgba(255, 255, 255, 0.8)",
    position: "fixed" as "fixed",
    top: 0,
    left: 0,
    width: "100%",
    zIndex: 9999,
  },
  spinner: {
    width: "60px",
    height: "60px",
    border: "8px solid #f3f3f3",
    borderTop: "8px solid #0070f3",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  message: {
    marginTop: "1rem",
    fontSize: "18px",
    color: "#333",
  },
};

// Add keyframes manually in your global CSS (see step 2 below)
