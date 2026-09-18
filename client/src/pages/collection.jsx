import React, { useState, useMemo, useEffect } from "react";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import { CollectionGrid } from "../ui/collection/collectionLayout";
import { getProducts } from "../services/productService";

const Collection = () => {
  const [selectedGender, setSelectedGender] = useState("all");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const loadAllProducts = async () => {
      try {
        const data = await getProducts();
        if (isMounted) setProducts(data);
      } catch (err) {
        console.error("Failed to load collection products:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    loadAllProducts();
    return () => {
      isMounted = false;
    };
  }, []);

  const womenProducts = useMemo(
    () => products.filter((p) => p.gender === "female"),
    [products],
  );
  const menProducts = useMemo(
    () => products.filter((p) => p.gender === "male"),
    [products],
  );

  const currentProducts = useMemo(() => {
    if (selectedGender === "women") return womenProducts;
    if (selectedGender === "men") return menProducts;
    return products;
  }, [selectedGender, womenProducts, menProducts, products]);

  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar bgstate={true} />

      <main className="flex-1 w-full pt-24 sm:pt-28">
        {/* Gender Toggle Selector */}
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
          <div className="flex items-center gap-3 border-b border-black/10 pb-4">
            <span className="text-xs uppercase tracking-wider text-neutral-400 font-medium mr-2">
              View:
            </span>
            <button
              onClick={() => setSelectedGender("all")}
              className={`px-4 py-1.5 text-xs sm:text-sm font-medium transition-colors cursor-pointer rounded-full ${
                selectedGender === "all"
                  ? "bg-black text-white"
                  : "bg-neutral-100 text-neutral-700 hover:bg-neutral-200"
              }`}
            >
              All Drops ({products.length})
            </button>
            <button
              onClick={() => setSelectedGender("women")}
              className={`px-4 py-1.5 text-xs sm:text-sm font-medium transition-colors cursor-pointer rounded-full ${
                selectedGender === "women"
                  ? "bg-black text-white"
                  : "bg-neutral-100 text-neutral-700 hover:bg-neutral-200"
              }`}
            >
              Women ({womenProducts.length})
            </button>
            <button
              onClick={() => setSelectedGender("men")}
              className={`px-4 py-1.5 text-xs sm:text-sm font-medium transition-colors cursor-pointer rounded-full ${
                selectedGender === "men"
                  ? "bg-black text-white"
                  : "bg-neutral-100 text-neutral-700 hover:bg-neutral-200"
              }`}
            >
              Men ({menProducts.length})
            </button>
          </div>
        </div>

        {loading ? (
          <div className="w-full max-w-7xl mx-auto px-4 py-24 text-center">
            <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-neutral-500 text-sm">
              Loading complete collection from database...
            </p>
          </div>
        ) : (
          <CollectionGrid
            products={currentProducts}
            title="Full Collection"
            subtitle="Explore the complete DROPP catalog across women's and men's seasonal collections directly from the database."
            availableCategories={["All", "Tops", "Bottoms", "Outerwear"]}
          />
        )}
      </main>

      <Footer />
    </div>
  );
};

export default Collection;
