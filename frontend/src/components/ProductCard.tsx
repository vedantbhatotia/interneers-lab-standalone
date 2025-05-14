import React from "react";
import { Product } from "data/products";

type Props = {
  product: Product;
  expanded: boolean;
  onClick: () => void;
};
export const ProductCard = ({ product, expanded, onClick }: Props) => {
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
      <h3>{product.name}</h3>
      {product.id}
      <p>Price: {product.price}</p>
      {expanded && (
        <div style={{ marginTop: "0.5rem" }}>
          <p>Stock:{product.stock}</p>
          <p>Description:{product.description}</p>
        </div>
      )}
    </div>
  );
};
