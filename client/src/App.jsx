import React from "react";
import {
  Landing,
  Men,
  Women,
  Collection,
  Sales,
  About,
  Carts,
  Login,
  Signup,
  Favourites,
  ProductDescription,
  BoughtProducts,
} from "./pages/pagesLayout";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ScrollToTop from "./hooks/scrollToTop";
import SuccessPayment from "./constants/successPayment";
import FailedPayment from "./constants/failedPayment";

const App = () => {
  return (
    <div className="flex items-center justify-center">
      <Router>
        <ScrollToTop />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/men-collection" element={<Men />} />
          <Route path="/women-collection" element={<Women />} />
          <Route path="/sales" element={<Sales />} />
          <Route path="/about" element={<About />} />
          <Route path="/collection" element={<Collection />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/carts" element={<Carts />} />
          <Route path="/bought-products" element={<BoughtProducts />} />
          <Route path="/favourites" element={<Favourites />} />
          <Route path="/product-description" element={<ProductDescription />} />
          <Route
            path="/product/:category/:id"
            element={<ProductDescription />}
          />
          <Route
            path="/payment/payment-successful"
            element={<SuccessPayment />}
          />
          <Route path="/payment/payment-failed" element={<FailedPayment />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
