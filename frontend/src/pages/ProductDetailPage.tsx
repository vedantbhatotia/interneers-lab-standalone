import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getProduct } from "api/products";
import LoadingSpinner from "components/LoadingSpinner";
import ErrorMessage from "components/ErrorMessage";

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  brand: string;
  category_object?: {
    id: string;
    title: string;
  };
}

export default function ProductDetailPage() {
  const { productId } = useParams<{ productId: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!productId) return;
    const fetchProduct = async () => {
      setLoading(true);
      try {
        const response = await getProduct(productId);
        setProduct(response.data);
        setError(null);
      } catch (err: any) {
        if (err.response?.status === 404) {
          setError("Product not found.");
        } else {
          setError(err.response?.data?.error || err.message);
        }
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [productId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!product) return <div>Product not found or no data available.</div>;

  return (
    <div style={{ maxWidth: 600, margin: "0 auto" }}>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>
        <strong>Price:</strong> ${product.price.toFixed(2)}
      </p>
      <p>
        <strong>Stock:</strong> {product.stock}
      </p>
      <p>
        <strong>Brand:</strong> {product.brand}
      </p>
      {product.category_object && (
        <p>
          <strong>Category:</strong>{" "}
          <Link to={`/categories/${product.category_object.id}`}>
            {product.category_object.title}
          </Link>
        </p>
      )}
    </div>
  );
}
