import React, { useState } from "react";
import { Product } from "data/products";
import { ProductCard } from "./ProductCard";

type Props = {
  products: Product[];
};

export const ProductList = ({ products }: Props) => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  return (
    <div className="max-w-3xl mx-auto p-4">
      {products.length === 0 ? (
        <p className="text-center text-gray-500">No products available.</p>
      ) : (
        products.map((prod: Product) => (
          <ProductCard
            key={prod.id}
            product={prod}
            expanded={prod.id === expandedId}
            onClick={() => {
              setExpandedId((prev) => (prev === prod.id ? null : prod.id));
            }}
          />
        ))
      )}
    </div>
  );
};
