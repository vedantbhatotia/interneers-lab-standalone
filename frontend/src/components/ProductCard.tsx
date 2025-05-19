import React from "react";
import { useNavigate } from "react-router-dom";
import { Product } from "data/products";

type Props = {
  product: Product;
  expanded: boolean;
  onClick: () => void;
};

export const ProductCard = ({ product, expanded, onClick }: Props) => {
  const navigate = useNavigate();

  return (
    <div
      onClick={onClick}
      className={`border rounded-lg p-4 mb-2 cursor-pointer transition 
        ${expanded ? "bg-gray-50 shadow-md" : "bg-white hover:shadow-sm"}`}
    >
      <h3 className="text-lg font-semibold text-gray-800">{product.name}</h3>
      <p className="text-gray-600">ID: {product.id}</p>
      <p className="text-gray-700 font-medium">Price: ${product.price}</p>

      {expanded && (
        <div className="mt-3">
          <p className="text-gray-600">Stock: {product.stock}</p>
          <p className="text-gray-600 mt-1">{product.description}</p>

          <button
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/products/${product.id}`);
            }}
            className="mt-4 inline-block px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
          >
            More..
          </button>
        </div>
      )}
    </div>
  );
};
