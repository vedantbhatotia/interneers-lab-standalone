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
  if (!category) return <div>Category not found or no data available.</div>;
  return (
    <div style={{ maxWidth: 800, margin: "0 auto" }}>
      <Link
        to="/categories"
        style={{ display: "inline-block", marginBottom: "0.5rem" }}
      >
        Back to CategoriesList
      </Link>
      {/* BreadCrumb Trail shows the current navigation path and helps the user to navigate in the directory structure */}
      <nav aria-label="breadcrumb" style={{ margin: "1rem 0" }}>
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/">Home</Link>
          </li>
          <li className="breadcrumb-item">
            <Link to="/categories">Categories</Link>
          </li>
          <li className="breadcrumb-item-active" aria-current="page">
            {category.title}
          </li>
        </ol>
      </nav>
      <h1>{category.title}</h1>
      <p>{category.description}</p>
      <h2>Products in “{category.title}”</h2>
      {products && products.length > 0 ? (
        <ProductList products={products} />
      ) : (
        <p>No products found in this category.</p>
      )}
    </div>
  );
}
