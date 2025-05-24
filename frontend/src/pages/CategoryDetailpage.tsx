import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getCategory } from "api/categories";
import { listProducts } from "api/products";
import LoadingSpinner from "components/LoadingSpinner";
import ErrorMessage from "components/ErrorMessage";
import { ProductList } from "components/ProductList";

interface Category {
  id: string;
  title: string;
  description: string;
}

export default function CategoryDetailPage() {
  const { categoryId } = useParams<{ categoryId: string }>();
  const [category, setCategory] = useState<Category | null>(null);
  const [products, setProducts] = useState<any[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!categoryId) return;
    const fetchData = async () => {
      setLoading(true);
      try {
        const catRes = await getCategory(categoryId);
        setCategory(catRes.data);
        const prodRes = await listProducts({ category: categoryId });
        setProducts(prodRes.data);
        setError(null);
      } catch (err: any) {
        if (err.response?.status === 404) {
          setError("Category not found.");
        } else {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [categoryId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!category)
    return (
      <div className="text-center text-gray-500 mt-10">
        Category not found or no data available.
      </div>
    );

  return (
    <div className="max-w-3xl mx-auto p-4">
      <Link
        to="/categories"
        className="inline-block mb-3 text-indigo-600 hover:text-indigo-800 transition"
      >
        &larr; Back to Categories List
      </Link>

      {/* Breadcrumb */}
      <nav className="mb-6 text-sm text-gray-600" aria-label="breadcrumb">
        <ol className="flex space-x-2">
          <li>
            <Link to="/" className="hover:underline hover:text-indigo-600">
              Home
            </Link>
            <span aria-hidden="true"> / </span>
          </li>
          <li>
            <Link
              to="/categories"
              className="hover:underline hover:text-indigo-600"
            >
              Categories
            </Link>
            <span aria-hidden="true"> / </span>
          </li>
          <li className="font-semibold text-gray-900" aria-current="page">
            {category.title}
          </li>
        </ol>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        {category.title}
      </h1>
      <p className="text-gray-700 mb-8">{category.description}</p>

      <h2 className="text-2xl font-semibold mb-4">
        Products in “{category.title}”
      </h2>

      {products && products.length > 0 ? (
        <ProductList products={products} />
      ) : (
        <p className="text-gray-500">No products found in this category.</p>
      )}
    </div>
  );
}
