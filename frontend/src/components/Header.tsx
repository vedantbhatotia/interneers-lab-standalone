import React from "react";
import { Link, useLocation } from "react-router-dom";

export const Header = () => {
  const location = useLocation();

  const navItems = [
    { label: "Home", path: "/" },
    { label: "Categories", path: "/categories" },
    { label: "Products", path: "/products" },
  ];

  return (
    <header className="bg-indigo-700 text-white shadow-md">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        {/* Logo / Brand */}
        <Link to="/" className="flex items-center space-x-2">
          <svg
            className="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M3 7v10a1 1 0 001 1h16a1 1 0 001-1V7" />
            <path d="M16 3h-8a1 1 0 00-1 1v3h10V4a1 1 0 00-1-1z" />
            <path d="M12 11v6" />
          </svg>
          <span className="text-xl font-bold tracking-wide">
            Product Catalog
          </span>
        </Link>

        {/* Navigation */}
        <nav>
          <ul className="flex space-x-6">
            {navItems.map(({ label, path }) => (
              <li key={path}>
                <Link
                  to={path}
                  className={`hover:text-indigo-300 transition font-medium ${
                    location.pathname === path
                      ? "underline decoration-indigo-300"
                      : ""
                  }`}
                >
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
};
