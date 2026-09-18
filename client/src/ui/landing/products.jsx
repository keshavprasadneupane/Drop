import React, { useState, useEffect } from "react";
import {
  SubHeading,
  DescriptionBlack,
  PricingText,
} from "../../components/componentsLayout";
import { useNavigate } from "react-router-dom";
import { getProducts } from "../../services/productService";

const Products = () => {
  const [womenProducts, setWomenProducts] = useState([]);
  const [menProducts, setMenProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const navigation = useNavigate();

  useEffect(() => {
    let isMounted = true;
    const loadProducts = async () => {
      try {
        const [women, men] = await Promise.all([
          getProducts("female"),
          getProducts("male"),
        ]);
        if (isMounted) {
          setWomenProducts(women);
          setMenProducts(men);
        }
      } catch (err) {
        console.error("Error loading products for landing:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadProducts();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="w-full py-10 sm:py-16 lg:py-20">
      {/* Women's Section */}
      <section className="w-full mb-8 sm:mb-large">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-start gap-1 sm:gap-mid mb-4 sm:mb-mid px-4 sm:pl-mid">
          <SubHeading headingName="Women’s New Arrivals" />
          <DescriptionBlack descriptionTexts="— Fresh fits, made with cotton" />
        </div>
        <div className="flex flex-row gap-3 sm:gap-mid overflow-x-auto px-4 sm:px-large pb-mid scrollbar-hide">
          {loading
            ? Array(4)
                .fill(0)
                .map((_, i) => (
                  <div
                    key={i}
                    className="w-40 sm:w-56 md:w-64 lg:w-70 shrink-0 animate-pulse"
                  >
                    <div className="w-full aspect-3/4 bg-neutral-200" />
                    <div className="h-4 bg-neutral-200 mt-2 w-3/4" />
                    <div className="h-4 bg-neutral-200 mt-1 w-1/2" />
                  </div>
                ))
            : womenProducts.map((product) => (
                <button
                  onClick={() =>
                    navigation("/product-description", { state: { product } })
                  }
                  key={product.id || product.item}
                  className="flex flex-col shrink-0 w-40 sm:w-56 md:w-64 lg:w-70 group cursor-pointer text-left"
                >
                  <div className="w-full aspect-3/4 overflow-hidden bg-neutral-100">
                    <img
                      src={product.image1}
                      alt={product.itemName}
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                  </div>
                  <div className="flex flex-col gap-1 mt-2 sm:mt-3">
                    <DescriptionBlack descriptionTexts={product.itemName} />
                    <div className="flex items-center justify-between">
                      <PricingText price={product.price} />
                      <span className="text-xs sm:text-sm">
                        ★ {product.ratings}
                      </span>
                    </div>
                  </div>
                </button>
              ))}
        </div>
      </section>

      {/* Men's Section */}
      <section className="w-full">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-start gap-1 sm:gap-mid mb-4 sm:mb-mid px-4 sm:pl-mid">
          <SubHeading headingName="Men’s New Arrivals" />
          <DescriptionBlack descriptionTexts="— Fresh fits, made with cotton" />
        </div>
        <div className="flex flex-row gap-3 sm:gap-mid overflow-x-auto px-4 sm:px-large pb-mid scrollbar-hide">
          {loading
            ? Array(4)
                .fill(0)
                .map((_, i) => (
                  <div
                    key={i}
                    className="w-40 sm:w-56 md:w-64 lg:w-70 shrink-0 animate-pulse"
                  >
                    <div className="w-full aspect-3/4 bg-neutral-200" />
                    <div className="h-4 bg-neutral-200 mt-2 w-3/4" />
                    <div className="h-4 bg-neutral-200 mt-1 w-1/2" />
                  </div>
                ))
            : menProducts.map((product) => (
                <button
                  onClick={() =>
                    navigation("/product-description", { state: { product } })
                  }
                  key={product.id || product.item}
                  className="flex flex-col shrink-0 w-40 sm:w-56 md:w-64 lg:w-70 group cursor-pointer text-left"
                >
                  <div className="w-full aspect-3/4 overflow-hidden bg-neutral-100">
                    <img
                      src={product.image1}
                      alt={product.itemName}
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                  </div>
                  <div className="flex flex-col gap-1 mt-2 sm:mt-3">
                    <DescriptionBlack descriptionTexts={product.itemName} />
                    <div className="flex items-center justify-between">
                      <PricingText price={product.price} />
                      <span className="text-xs sm:text-sm">
                        ★ {product.ratings}
                      </span>
                    </div>
                  </div>
                </button>
              ))}
        </div>
      </section>
    </div>
  );
};

export default Products;
