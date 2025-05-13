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
  // placeholder when there are no products
  if (!products) return null;
  return <ProductList products={products} />;
}
