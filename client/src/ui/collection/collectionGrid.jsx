import React, { useMemo, useState } from "react";
import ProductCard from "./productCard";
import FilterBar from "./filterBar";

const CollectionGrid = ({
  products = [],
  title = "Collection",
  subtitle = "Discover our latest drops and timeless wardrobe staples.",
  bannerImage = null,
  isSalePage = false,
  availableCategories = ["All", "Tops", "Bottoms", "Outerwear"],
}) => {
  const [activeCategory, setActiveCategory] = useState("All");
  const [sortOption, setSortOption] = useState("featured");
  const [searchQuery, setSearchQuery] = useState("");

  // Helper to categorize items
  const categorizeItem = (name = "") => {
    const lower = name.toLowerCase();
    if (
      lower.includes("pants") ||
      lower.includes("jeans") ||
      lower.includes("cargo") ||
      lower.includes("skirt") ||
      lower.includes("sweatpants") ||
      lower.includes("chino")
    ) {
      return "Bottoms";
    }
    if (
      lower.includes("jacket") ||
      lower.includes("blazer") ||
      lower.includes("coat") ||
      lower.includes("bomber") ||
      lower.includes("overshirt")
    ) {
      return "Outerwear";
    }
    if (
      lower.includes("shirt") ||
      lower.includes("hoodie") ||
      lower.includes("tank") ||
      lower.includes("polo") ||
      lower.includes("sweatshirt") ||
      lower.includes("top") ||
      lower.includes("dress") ||
      lower.includes("cardigan")
    ) {
      return "Tops";
    }
    return "Other";
  };

  const filteredAndSortedProducts = useMemo(() => {
    let result = [...products];

    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(
        (p) =>
          p.itemName.toLowerCase().includes(q) ||
          (p.description && p.description.toLowerCase().includes(q)),
      );
    }

    // Category filter
    if (activeCategory !== "All") {
      result = result.filter(
        (p) => categorizeItem(p.itemName) === activeCategory,
      );
    }

    const parseVal = (str) =>
      parseFloat(
        String(str || "")
          .replace(/,/g, "")
          .replace(/[^0-9.]/g, ""),
      ) || 0;

    // Sorting
    if (sortOption === "price-asc") {
      result.sort((a, b) => parseVal(a.price) - parseVal(b.price));
    } else if (sortOption === "price-desc") {
      result.sort((a, b) => parseVal(b.price) - parseVal(a.price));
    } else if (sortOption === "rating") {
      result.sort(
        (a, b) => (parseFloat(b.ratings) || 0) - (parseFloat(a.ratings) || 0),
      );
    } else if (sortOption === "name") {
      result.sort((a, b) => a.itemName.localeCompare(b.itemName));
    }

    return result;
  }, [products, activeCategory, sortOption, searchQuery]);

  return (
    <div className="w-full flex flex-col">
      {/* Optional Hero Banner */}
      {bannerImage && (
        <div className="relative w-full h-64 sm:h-80 lg:h-96 overflow-hidden bg-black">
          <img
            src={bannerImage}
            alt={title}
            className="w-full h-full object-cover opacity-70"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent flex flex-col justify-end p-6 sm:p-10 lg:p-16">
            <h1 className="font-poppins font-medium text-3xl sm:text-4xl lg:text-5xl text-white">
              {title}
            </h1>
            <p className="font-poppins font-light text-sm sm:text-base text-white/80 max-w-xl mt-2">
              {subtitle}
            </p>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {!bannerImage && (
          <div className="mb-6">
            <h1 className="font-poppins font-medium text-2xl sm:text-3xl lg:text-4xl text-neutral-900">
              {title}
            </h1>
            <p className="font-poppins font-light text-sm sm:text-base text-neutral-600 mt-1">
              {subtitle}
            </p>
          </div>
        )}

        {/* Filter / Sort Bar */}
        <FilterBar
          categories={availableCategories}
          activeCategory={activeCategory}
          onSelectCategory={setActiveCategory}
          sortOption={sortOption}
          onSelectSort={setSortOption}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          totalItems={filteredAndSortedProducts.length}
        />

        {/* Product Grid or Empty State */}
        {filteredAndSortedProducts.length === 0 ? (
          <div className="w-full py-20 flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 rounded-full bg-neutral-100 flex items-center justify-center text-2xl text-neutral-400 mb-4">
              🔍
            </div>
            <h3 className="font-poppins font-medium text-lg text-neutral-900">
              No products found
            </h3>
            <p className="font-poppins text-sm text-neutral-500 max-w-md mt-1 mb-6">
              We couldn't find anything matching your filters. Try clearing your
              search or switching categories.
            </p>
            <button
              onClick={() => {
                setActiveCategory("All");
                setSearchQuery("");
              }}
              className="px-6 py-2 bg-black text-white text-xs sm:text-sm font-poppins cursor-pointer hover:bg-neutral-800 transition-colors"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8 pt-8">
            {filteredAndSortedProducts.map((product, idx) => (
              <ProductCard
                key={`${product.item}-${idx}`}
                product={product}
                isSaleItem={isSalePage}
                discountPercent={isSalePage ? (idx % 2 === 0 ? 25 : 15) : 0}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CollectionGrid;
