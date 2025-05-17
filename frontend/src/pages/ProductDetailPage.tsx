import React, { useState, useEffect, FormEvent } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getProduct, updateProduct, deleteProduct } from "api/products";
import { listCategories } from "api/categories";
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
export interface Category {
  id: string;
  title: string;
}
export default function ProductDetailPage() {
  const { productId } = useParams<{ productId: string }>();
  const navigate = useNavigate();

  const [product, setProduct] = useState<Product | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState<boolean>(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const [formState, setFormState] = useState({
    name: "",
    description: "",
    price: 0,
    stock: 0,
    brand: "",
    category: "",
  });

  useEffect(() => {
    if (!productId) return;
    const fetchData = async () => {
      setLoading(true);
      try {
        const res = await getProduct(productId);
        const data = res.data;
        setProduct(data);
        setFormState({
          name: data.name,
          description: data.description,
          price: data.price,
          stock: data.stock,
          brand: data.brand,
          category: data.category_object?.id || "",
        });
        const cats = await listCategories();
        setCategories(cats.data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [productId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!product) return <div>Product not found or no data available.</div>;

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormState((prev) => ({
      ...prev,
      [name]: name === "price" || name === "stock" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const payload = {
        name: formState.name,
        description: formState.description,
        price: formState.price,
        stock: formState.stock,
        brand: formState.brand,
        category: formState.category,
      };
      const res = await updateProduct(productId!, payload);
      setProduct(res.data);
      const updated = res.data;
      setFormState({
        name: updated.name,
        description: updated.description,
        price: updated.price,
        stock: updated.stock,
        brand: updated.brand,
        category: updated.category_object?.id || "",
      });
      setSuccessMessage("Product updated successfully.");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this product?"))
      return;
    try {
      await deleteProduct(productId!);
      navigate("/products");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto" }}>
      <Link to="/products">Back to Products</Link>
      <h1>Edit Product</h1>
      {successMessage && (
        <div className="success-message">{successMessage}</div>
      )}
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={formState.name}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Description:
          <input
            type="text"
            name="description"
            value={formState.description}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Price:
          <input
            type="number"
            name="price"
            value={formState.price}
            onChange={handleChange}
            step="0.01"
            required
          />
        </label>
        <label>
          Stock:
          <input
            type="number"
            name="stock"
            value={formState.stock}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Brand:
          <input
            type="text"
            name="brand"
            value={formState.brand}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Category:
          <select
            name="category"
            value={formState.category}
            onChange={handleChange}
            required
          >
            <option value="">-- Select a category --</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </label>
        <button type="submit" disabled={saving}>
          {saving ? "Saving..." : "Save Changes"}
        </button>
      </form>
      <button onClick={handleDelete} style={{ marginTop: 16, color: "red" }}>
        Delete Product
      </button>
      {error && <ErrorMessage message={error} />}
    </div>
  );
}
