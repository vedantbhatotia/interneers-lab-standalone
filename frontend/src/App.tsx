import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Header } from "components/Header";
import { NavBar } from "components/NavBar";
import { ProductList } from "components/ProductList";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);
const About = () => (
  <div>
    <h2>About</h2>
  </div>
);
function App() {
  return (
    <>
      <Router>
        <Header></Header>
        <NavBar></NavBar>
        <main style={{ padding: "1rem" }}>
          <Routes>
            <Route path="/home" element={<Home></Home>}></Route>
            <Route
              path="/products"
              element={<ProductList></ProductList>}
            ></Route>
            <Route path="/about" element={<About></About>}></Route>
          </Routes>
        </main>
      </Router>
    </>
  );
}

export default App;
