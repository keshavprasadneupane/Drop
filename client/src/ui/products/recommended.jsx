import React from "react";
import { SimilarProducts } from "../../utils/recommendedProducts";
import { useNavigate } from "react-router-dom";

const RecommendedProducts = () => {
  const navigate = useNavigate();

  return (
    <section className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 border-t border-black/10">
      <div className="flex flex-col sm:flex-row items-start sm:items-baseline justify-between gap-1 mb-6">
        <div>
          <h2 className="font-poppins font-medium text-xl sm:text-2xl text-neutral-900">
            Recommended For You
          </h2>
          <p className="font-poppins text-xs sm:text-sm text-neutral-500 mt-0.5">
            Handpicked essentials that pair effortlessly
          </p>
        </div>
        <button
          onClick={() => navigate("/collection")}
          className="text-xs font-poppins text-neutral-600 hover:text-black underline cursor-pointer"
        >
          View all
        </button>
      </div>

      <div className="flex flex-row gap-4 sm:gap-6 overflow-x-auto pb-4 scrollbar-hide">
        {SimilarProducts.map((product) => (
          <div
            key={product.item}
            onClick={() => {
              navigate("/product-description", { state: { product } });
              window.scrollTo(0, 0);
            }}
            className="flex flex-col shrink-0 w-44 sm:w-56 md:w-64 group cursor-pointer text-left"
          >
            <div className="w-full aspect-3/4 overflow-hidden bg-neutral-100">
              <img
                src={product.image1}
                alt={product.itemName}
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
            </div>

            <div className="flex flex-col gap-1 mt-3">
              <h3 className="font-poppins font-medium text-xs sm:text-sm text-neutral-900 truncate group-hover:text-blue-600 transition-colors">
                {product.itemName}
              </h3>

              <div className="flex items-center justify-between text-xs sm:text-sm">
                <span className="font-poppins font-semibold text-neutral-900">
                  {product.price}
                </span>
                <span className="text-neutral-500">★ {product.ratings}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RecommendedProducts;
