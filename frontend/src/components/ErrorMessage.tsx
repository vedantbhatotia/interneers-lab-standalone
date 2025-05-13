import React from "react";
type Props = {
  message: string;
};
export default function ErrorMessage({ message }: Props) {
  return (
    <div
      style={{
        padding: "1rem",
        backgroundColor: "#ffe6e6",
        color: "#cc0000",
        border: "1px solid #cc0000",
        borderRadius: "8px",
        margin: "1rem 0",
        textAlign: "center",
      }}
    >
      <strong>Error:</strong> {message}
    </div>
  );
}
