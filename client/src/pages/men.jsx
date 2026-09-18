import React, { useState, useEffect } from "react";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import { CollectionGrid } from "../ui/collection/collectionLayout";
import { getProducts } from "../services/productService";
import MenBanner from "../assets/images/menArrivals.jpg";

const Men = () => {
  const [menProducts, setMenProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const fetchMen = async () => {
      try {
        const data = await getProducts("male");
        if (isMounted) setMenProducts(data);
      } catch (err) {
        console.error("Failed to load men collection:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchMen();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar />
      <main className="flex-1 w-full">
        {loading ? (
          <div className="w-full max-w-7xl mx-auto px-4 py-24 text-center">
            <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-neutral-500 text-sm">
              Loading Men's Collection from database...
            </p>
          </div>
        ) : (
          <CollectionGrid
            products={menProducts}
            title="Men's Collection"
            subtitle="Engineered for daily versatility. Clean cuts, heavyweight cottons, and elevated streetwear."
            bannerImage={MenBanner}
            availableCategories={["All", "Tops", "Bottoms", "Outerwear"]}
          />
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Men;
