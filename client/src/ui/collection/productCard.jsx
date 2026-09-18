import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import useFavs from "../../hooks/favs";
import { useToast } from "../../hooks/toast";

const ProductCard = ({ product, isSaleItem = false, discountPercent = 20 }) => {
  const navigate = useNavigate();
  const { toggleFavourite, isFavourite } = useFavs();
  const { showToast } = useToast();
  const [isHovered, setIsHovered] = useState(false);

  const isFav = isFavourite(product);

  const handleToggleFav = (e) => {
    e.stopPropagation();
    toggleFavourite(product);
    if (isFav) {
      showToast("Removed from favourites", "info");
    } else {
      showToast(`Added ${product.itemName} to favourites ♥`, "success");
    }
  };

  const handleCardClick = () => {
    navigate("/product-description", { state: { product } });
  };

  // Calculate discounted price if sale
  const numericPrice =
    parseFloat(
      String(product.price || "")
        .replace(/,/g, "")
        .replace(/[^0-9.]/g, ""),
    ) || 0;
  const salePrice = isSaleItem
    ? `Rs. ${Math.round(numericPrice * (1 - discountPercent / 100)).toLocaleString()}`
    : null;

  return (
    <div
      onClick={handleCardClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="group flex flex-col cursor-pointer transition-all duration-300 relative"
    >
      {/* Product Image Container */}
      <div className="relative w-full aspect-3/4 overflow-hidden bg-neutral-100 rounded-sm">
        {/* Primary and Hover Image */}
        <img
          src={product.image1}
          alt={product.itemName}
          className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-500 ease-in-out ${
            isHovered && product.image2
              ? "opacity-0 scale-105"
              : "opacity-100 scale-100"
          }`}
        />
        {product.image2 && (
          <img
            src={product.image2}
            alt={`${product.itemName} alternate view`}
            className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-500 ease-in-out ${
              isHovered ? "opacity-100 scale-105" : "opacity-0 scale-100"
            }`}
          />
        )}

        {/* Sale Badge */}
        {isSaleItem && (
          <span className="absolute top-2.5 left-2.5 bg-red-600 text-white text-[11px] font-poppins font-medium px-2 py-0.5 tracking-wider uppercase shadow-sm">
            SALE -{discountPercent}%
          </span>
        )}

        {/* Favourite Button */}
        <button
          type="button"
          onClick={handleToggleFav}
          aria-label={isFav ? "Remove from favourites" : "Add to favourites"}
          className={`absolute top-2.5 right-2.5 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 shadow-md ${
            isFav
              ? "bg-red-600 text-white scale-110"
              : "bg-white/90 text-neutral-800 hover:bg-white hover:scale-110 opacity-90 sm:opacity-0 sm:group-hover:opacity-100"
          }`}
        >
          {isFav ? "♥" : "♡"}
        </button>

        {/* Quick size preview bar on hover */}
        {product.availableSizes && (
          <div
            className={`absolute bottom-0 inset-x-0 bg-black/75 backdrop-blur-xs py-2 px-2 flex items-center justify-center gap-1.5 transition-transform duration-300 ${
              isHovered ? "translate-y-0" : "translate-y-full"
            }`}
          >
            <span className="text-[10px] text-white/70 uppercase tracking-widest mr-1">
              Sizes:
            </span>
            {product.availableSizes.slice(0, 5).map((size) => (
              <span
                key={size}
                className="text-[10px] font-medium text-white px-1 py-0.5 border border-white/30 rounded-xs"
              >
                {size}
              </span>
            ))}
            {product.availableSizes.length > 5 && (
              <span className="text-[10px] text-white/70">
                +{product.availableSizes.length - 5}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Details Section */}
      <div className="flex flex-col gap-1 mt-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-poppins font-medium text-sm sm:text-base text-neutral-900 line-clamp-1 group-hover:text-blue-600 transition-colors">
            {product.itemName}
          </h3>
          <span className="flex items-center gap-0.5 text-xs text-neutral-600 font-poppins shrink-0">
            <span className="text-amber-500">★</span> {product.ratings}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {isSaleItem ? (
            <>
              <span className="font-poppins font-semibold text-sm sm:text-base text-red-600">
                {salePrice}
              </span>
              <span className="font-poppins text-xs sm:text-sm text-neutral-400 line-through">
                {product.price}
              </span>
            </>
          ) : (
            <span className="font-poppins font-medium text-sm sm:text-base text-neutral-900">
              {product.price}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
