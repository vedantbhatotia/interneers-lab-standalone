import React from "react";
import { Link } from "react-router-dom";
export const NavBar = () => (
  <nav
    style={{
      display: "flex",
      justifyContent: "center",
      gap: "2rem",
      padding: "0.5rem",
      background: "#f0f0f0",
    }}
  >
    <Link to="/">Home</Link>
    <Link to="/products">Products</Link>
    <Link to="/about">About</Link>
    <Link to="/categories">Categories</Link>
  </nav>
);
