import React, { useState } from "react";
import { Product, products } from "data/products";
import { ProductCard } from "./ProductCard";
export const ProductList = () => {
  const [expandedId, setExpandedId] = useState<number | null>(null);
  return (
    <div>
      {products.map((prod: Product) => (
        <ProductCard
          key={prod.id}
          product={prod}
          expanded={prod.id === expandedId}
          onClick={() => {
            setExpandedId((prev) => (prev === prod.id ? null : prod.id));
          }}
        ></ProductCard>
      ))}
    </div>
  );
};
