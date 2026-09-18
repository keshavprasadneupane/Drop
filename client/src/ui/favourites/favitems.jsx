import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import useFavs from "../../hooks/favs";
import useCart from "../../hooks/carts";
import { useToast } from "../../hooks/toast";

const FavItems = () => {
  const { favList, removeFromFavourites, setFavList } = useFavs();
  const { addToCart } = useCart();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [activeSizeItem, setActiveSizeItem] = useState(null);

  const handleRemove = (index, name) => {
    removeFromFavourites(index);
    showToast(`Removed ${name} from favourites`, "info");
  };

  const handleMoveToCart = (product, size) => {
    const chosenSize =
      size || (product.availableSizes && product.availableSizes[0]) || "M";
    addToCart(product, chosenSize);
    showToast(`Added ${product.itemName} (${chosenSize}) to bag!`, "success");
    setActiveSizeItem(null);
  };

  if (favList.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center w-full min-h-[60vh] gap-4 px-4 py-16 text-center">
        <div className="w-20 h-20 rounded-full bg-neutral-100 flex items-center justify-center text-3xl mb-2">
          ♡
        </div>
        <h2 className="font-poppins font-medium text-2xl text-neutral-900">
          Your wishlist is empty
        </h2>
        <p className="font-poppins font-light text-sm sm:text-base text-neutral-500 max-w-sm">
          Save your favourite items by tapping the heart icon while exploring
          our drops.
        </p>
        <button
          onClick={() => navigate("/collection")}
          className="mt-4 bg-black text-white px-8 py-3 text-sm font-poppins font-medium hover:bg-neutral-800 transition-colors cursor-pointer"
        >
          Explore Collection
        </button>
      </div>
    );
  }

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-16">
      <div className="flex items-center justify-between mb-8 sm:mb-10 pb-4 border-b border-black/10">
        <div>
          <h1 className="font-poppins font-medium text-2xl sm:text-3xl text-neutral-900">
            Favourites
          </h1>
          <p className="text-xs sm:text-sm text-neutral-500 font-poppins mt-1">
            {favList.length} {favList.length === 1 ? "item" : "items"} saved to
            your wishlist
          </p>
        </div>

        {favList.length > 0 && (
          <button
            onClick={() => {
              setFavList([]);
              showToast("Cleared all favourites", "info");
            }}
            className="text-xs font-poppins text-neutral-500 hover:text-red-600 transition-colors underline cursor-pointer"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8">
        {favList.map((product, index) => (
          <div
            key={`${product.item}-${index}`}
            className="flex flex-col group bg-white border border-black/5 hover:border-black/20 transition-all p-2 rounded-xs"
          >
            {/* Image Box */}
            <div className="relative w-full aspect-3/4 overflow-hidden bg-neutral-100">
              <img
                src={product.image1}
                alt={product.itemName}
                onClick={() =>
                  navigate("/product-description", { state: { product } })
                }
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105 cursor-pointer"
              />

              {/* Remove button */}
              <button
                onClick={() => handleRemove(index, product.itemName)}
                aria-label="Remove from favourites"
                className="absolute top-2 right-2 w-7 h-7 flex items-center justify-center bg-white/90 text-neutral-700 text-xs rounded-full hover:bg-red-600 hover:text-white transition-colors cursor-pointer shadow-xs"
              >
                ✕
              </button>
            </div>

            {/* Product Details */}
            <div className="flex flex-col gap-1.5 mt-3 px-1">
              <h3
                onClick={() =>
                  navigate("/product-description", { state: { product } })
                }
                className="font-poppins font-medium text-sm sm:text-base text-neutral-900 truncate cursor-pointer hover:text-blue-600 transition-colors"
              >
                {product.itemName}
              </h3>

              <div className="flex items-center justify-between text-xs sm:text-sm">
                <span className="font-poppins font-semibold text-neutral-900">
                  {product.price}
                </span>
                <span className="text-neutral-500">★ {product.ratings}</span>
              </div>

              {/* Move to bag button */}
              <div className="mt-2 pt-2 border-t border-black/5">
                {activeSizeItem === index ? (
                  <div className="flex flex-col gap-1.5">
                    <span className="text-[10px] uppercase font-poppins text-neutral-500">
                      Choose Size:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {(product.availableSizes || ["S", "M", "L", "XL"]).map(
                        (size) => (
                          <button
                            key={size}
                            onClick={() => handleMoveToCart(product, size)}
                            className="px-2 py-1 text-xs border border-black/20 hover:border-black hover:bg-black hover:text-white transition-colors font-poppins cursor-pointer"
                          >
                            {size}
                          </button>
                        ),
                      )}
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={() => setActiveSizeItem(index)}
                    className="w-full bg-black text-white text-xs font-poppins font-medium py-2 px-3 hover:bg-neutral-800 transition-colors cursor-pointer"
                  >
                    Move to Bag
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FavItems;
