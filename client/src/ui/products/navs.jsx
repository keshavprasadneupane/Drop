import React from "react";
import { Link } from "react-router-dom";

const Navs = () => {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 flex items-center gap-2 text-xs sm:text-sm text-neutral-500 font-poppins">
      <Link to="/" className="hover:text-black transition-colors">
        Home
      </Link>
      <span>/</span>
      <Link to="/collection" className="hover:text-black transition-colors">
        Collection
      </Link>
      <span>/</span>
      <span className="text-black font-medium">Product Details</span>
    </div>
  );
};

export default Navs;
