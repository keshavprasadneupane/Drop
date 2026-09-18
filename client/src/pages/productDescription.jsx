import React from "react";
import Footer from "../constants/footer";
import Navbar from "../constants/navbar";
import CustomerReview from "../ui/products/customerReview";
import Navs from "../ui/products/navs";
import ProductDetails from "../ui/products/productDetails";
import RecommendedProducts from "../ui/products/recommended";

const ProductDescription = () => {
  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar bgstate={true} />
      <main className="flex-1 w-full pt-16 sm:pt-20">
        <Navs />
        <ProductDetails />
        <RecommendedProducts />
        <CustomerReview />
      </main>
      <Footer />
    </div>
  );
};

export default ProductDescription;
