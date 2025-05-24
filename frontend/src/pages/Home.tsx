import React from "react";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-indigo-50 to-white p-6">
      <h1 className="text-5xl font-extrabold text-indigo-700 mb-6 text-center">
        Welcome to Your Product Store
      </h1>
      <p className="max-w-xl text-center text-gray-700 mb-10">
        Explore a wide range of product categories and find detailed product
        information. Click below to browse categories or see all products.
      </p>

      <div className="flex space-x-6">
        <Link
          to="/categories"
          className="px-6 py-3 bg-indigo-600 text-white rounded-md text-lg font-semibold hover:bg-indigo-700 transition"
        >
          Browse Categories
        </Link>

        <Link
          to="/products"
          className="px-6 py-3 border border-indigo-600 text-indigo-600 rounded-md text-lg font-semibold hover:bg-indigo-100 transition"
        >
          View All Products
        </Link>
      </div>

      <footer className="mt-auto pt-10 text-gray-400 text-sm">
        &copy; {new Date().getFullYear()} Your Company. All rights reserved.
      </footer>
    </div>
  );
}
