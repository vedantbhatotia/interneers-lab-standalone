import React from "react";
import "./App.css";
import { Header } from "components/Header";
import { NavBar } from "components/NavBar";
import ProductListPage from "pages/ProductListPage";
import CategoryListPage from "pages/CategoryListPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <>
      <Router>
        <Header></Header>
        <NavBar></NavBar>
        <main style={{ padding: "1rem" }}>
          <Routes>
            <Route
              path="/products"
              element={<ProductListPage></ProductListPage>}
            ></Route>
            <Route
              path="/categories"
              element={<CategoryListPage></CategoryListPage>}
            ></Route>
            {/* <Route path="/home" element={<Home></Home>}></Route>
            <Route path="/about" element={<About></About>}></Route> */}
          </Routes>
        </main>
      </Router>
    </>
  );
}

export default App;
