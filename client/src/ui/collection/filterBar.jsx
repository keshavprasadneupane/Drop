import React from "react";

const FilterBar = ({
  categories = [],
  activeCategory = "All",
  onSelectCategory,
  sortOption = "featured",
  onSelectSort,
  searchQuery = "",
  onSearchChange,
  totalItems = 0,
}) => {
  return (
    <div className="w-full flex flex-col gap-4 py-4 border-b border-black/10">
      {/* Top row: Category tags & search */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Category Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-hide">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => onSelectCategory(cat)}
              className={`px-4 py-1.5 text-xs sm:text-sm font-poppins transition-all duration-200 whitespace-nowrap cursor-pointer rounded-full ${
                activeCategory === cat
                  ? "bg-black text-white font-medium shadow-xs"
                  : "bg-neutral-100 text-neutral-600 hover:bg-neutral-200"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Search input */}
        <div className="relative w-full md:w-64">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search products..."
            className="w-full bg-neutral-50 border border-black/15 rounded-full px-4 py-1.5 pl-9 text-xs sm:text-sm font-poppins text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:border-black transition-colors"
          />
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          {searchQuery && (
            <button
              onClick={() => onSearchChange("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-700 text-xs"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Bottom row: Item count & Sort dropdown */}
      <div className="flex items-center justify-between pt-2 text-xs sm:text-sm text-neutral-500 font-poppins">
        <span>
          Showing <strong className="text-black">{totalItems}</strong> {totalItems === 1 ? "item" : "items"}
        </span>

        <div className="flex items-center gap-2">
          <label htmlFor="sort-select" className="text-neutral-600">
            Sort by:
          </label>
          <select
            id="sort-select"
            value={sortOption}
            onChange={(e) => onSelectSort(e.target.value)}
            className="bg-transparent border border-black/20 rounded-md px-2.5 py-1 text-xs sm:text-sm text-neutral-900 font-poppins focus:outline-none focus:border-black cursor-pointer"
          >
            <option value="featured">Featured</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="rating">Highest Rated</option>
            <option value="name">Name (A-Z)</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default FilterBar;

