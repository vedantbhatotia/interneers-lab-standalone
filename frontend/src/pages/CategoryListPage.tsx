import React, { useState, useEffect } from "react";
import { listCategories } from "api/categories";
import LoadingSpinner from "components/LoadingSpinner";
import ErrorMessage from "components/ErrorMessage";
import { CategoryList } from "components/CategoryList";
type Category = {
  id: string;
  title: string;
  description: string;
};
export default function CategoryListPage() {
  const [categories, setCategories] = useState<Category[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      setLoading(true);
      try {
        const result = await listCategories();
        setCategories(result.data);
        setError(null);
      } catch (err: any) {
        setError(err.response?.data?.error || err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, []);
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  // placeholder when there are no products
  if (!categories) return null;
  return <CategoryList categories={categories} />;
}
