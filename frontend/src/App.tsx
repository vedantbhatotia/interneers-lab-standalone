import React from "react";
import "./App.css";
import { Header } from "components/Header";
// import { NavBar } from "components/NavBar";
import ProductListPage from "pages/ProductListPage";
import CategoryListPage from "pages/CategoryListPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProductDetailPage from "pages/ProductDetailPage";
import CategoryDetailPage from "pages/CategoryDetailpage";
import HomePage from "pages/Home";
function App() {
  return (
    <>
      <Router>
        <Header></Header>
        {/* <NavBar></NavBar> */}
        <main style={{ padding: "1rem" }}>
          <Routes>
            <Route path="/" element={<HomePage></HomePage>}></Route>
            <Route
              path="/products"
              element={<ProductListPage></ProductListPage>}
            ></Route>
            <Route
              path="/categories"
              element={<CategoryListPage></CategoryListPage>}
            ></Route>
            <Route
              path="/products/:productId"
              element={<ProductDetailPage></ProductDetailPage>}
            ></Route>
            <Route
              path="/categories/:categoryId"
              element={<CategoryDetailPage></CategoryDetailPage>}
            ></Route>
          </Routes>
        </main>
      </Router>
    </>
  );
}

export default App;
