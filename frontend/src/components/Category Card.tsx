import React from "react";

type Props = {
  category: {
    id: string;
    title: string;
    description: string;
  };
  expanded: boolean;
  onClick: () => void;
};

export const CategoryCard = ({ category, expanded, onClick }: Props) => {
  return (
    <div
      onClick={onClick}
      style={{
        border: "1px solid #ccc",
        borderRadius: 8,
        padding: "1rem",
        marginBottom: "0.5rem",
        cursor: "pointer",
        background: expanded ? "#f9f9f9" : "#fff",
      }}
    >
      <h3>{category.title}</h3>
      {/* {category.id} */}
      {expanded && (
        <div style={{ marginTop: "0.5rem" }}>
          <p>{category.description}</p>
        </div>
      )}
      {/* {category.id} */}
    </div>
  );
};
