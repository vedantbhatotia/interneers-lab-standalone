import React, { useState, useEffect } from "react";
import { listProducts } from "api/products";
import LoadingSpinner from "components/LoadingSpinner";
import ErrorMessage from "components/ErrorMessage";
import { ProductList } from "components/ProductList";
import { Product } from "data/products";

export default function ProductListPage() {
  const [products, setProducts] = useState<Product[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const result = await listProducts();
        setProducts(result.data);
        setError(null);
      } catch (err: any) {
        setError(err.response?.data?.error || err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  if (!products)
    return (
      <div className="max-w-3xl mx-auto p-4 text-center text-gray-500 mt-10">
        No products available.
      </div>
    );

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Products</h1>
      <ProductList products={products} />
    </div>
  );
}
