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

  if (!categories)
    return (
      <div className="max-w-3xl mx-auto p-4 text-center text-gray-500 mt-10">
        No categories available.
      </div>
    );

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">Categories</h1>
      <CategoryList categories={categories} />
    </div>
  );
}
