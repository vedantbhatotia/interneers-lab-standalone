import React from "react";
export default function LoadingSpinner() {
  return (
    <div style={spinnerContainer}>
      <div style={spinner} />
    </div>
  );
}
const spinnerContainer = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  padding: "2rem",
};

const spinner = {
  width: "3rem",
  height: "3rem",
  border: "4px solid rgba(0, 0, 0, 0.1)",
  borderTop: "4px solid #333",
  borderRadius: "50%",
  animation: "spin 1s linear infinite",
};
