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
  category_object?: { id: string; title: string };
}

export default function ProductDetailPage() {
  const { productId } = useParams<{ productId: string }>();
  const navigate = useNavigate();

  const [product, setProduct] = useState<Product | null>(null);
  const [categories, setCategories] = useState<{ id: string; title: string }[]>(
    [],
  );
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
    setLoading(true);
    (async () => {
      try {
        const res = await getProduct(productId);
        const data = res.data as Product;
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
        setError(err.response?.data?.error || err.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [productId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!product)
    return (
      <div className="text-center py-8">
        Product not found or no data available.
      </div>
    );

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
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
      const res = await updateProduct(productId!, formState);
      setProduct(res.data);
      setSuccessMessage("Product updated successfully.");
    } catch (err: any) {
      setError(err.response?.data?.error || err.message);
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
      setError(err.response?.data?.error || err.message);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md mt-8">
      <Link
        to="/products"
        className="inline-block text-blue-600 hover:underline mb-4"
      >
        &larr; Back to Products
      </Link>

      <nav className="text-gray-600 text-sm mb-6">
        <Link to="/">Home</Link> / <Link to="/products">Products</Link> /{" "}
        <span className="font-medium">{product.name}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        Edit Product: {product.name}
      </h1>

      {product.category_object && (
        <p className="text-gray-700 mb-4">
          Category:{" "}
          <Link
            to={`/categories/${product.category_object.id}`}
            className="text-blue-600 hover:underline"
          >
            {product.category_object.title}
          </Link>
        </p>
      )}

      {successMessage && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded mb-4">
          {successMessage}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <div>
          <label className="block text-gray-700 mb-1">Name</label>
          <input
            type="text"
            name="name"
            value={formState.name}
            onChange={handleChange}
            required
            className="w-full border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Brand</label>
          <input
            type="text"
            name="brand"
            value={formState.brand}
            onChange={handleChange}
            required
            className="w-full border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Description</label>
          <input
            type="text"
            name="description"
            value={formState.description}
            onChange={handleChange}
            required
            className="w-full border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Category</label>
          <select
            name="category"
            value={formState.category}
            onChange={handleChange}
            required
            className="w-full border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">-- Select a category --</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Price</label>
          <input
            type="number"
            name="price"
            value={formState.price}
            onChange={handleChange}
            step="0.01"
            required
            className="w-full border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Stock</label>
          <input
            type="number"
            name="stock"
            value={formState.stock}
            onChange={handleChange}
            required
            className="w-full border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="md:col-span-2 flex space-x-4">
          <button
            type="submit"
            disabled={saving}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
          <button
            type="button"
            onClick={handleDelete}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Delete Product
          </button>
        </div>
      </form>

      {error && <ErrorMessage message={error} />}
    </div>
  );
}
