import React, { useState, useEffect } from "react";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import { CollectionGrid } from "../ui/collection/collectionLayout";
import { getProducts } from "../services/productService";

const Sales = () => {
  const [saleProducts, setSaleProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Simulated countdown timer for sale urgency
  const [timeLeft, setTimeLeft] = useState({
    hours: 14,
    minutes: 32,
    seconds: 45,
  });

  useEffect(() => {
    let isMounted = true;
    const loadSaleItems = async () => {
      try {
        const all = await getProducts();
        if (isMounted) {
          // Curate items for the seasonal sale
          const selected = all.filter((_, idx) => idx % 2 === 0).slice(0, 12);
          setSaleProducts(selected);
        }
      } catch (err) {
        console.error("Failed to load sale products:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    loadSaleItems();
    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev.seconds > 0) {
          return { ...prev, seconds: prev.seconds - 1 };
        } else if (prev.minutes > 0) {
          return { ...prev, minutes: prev.minutes - 1, seconds: 59 };
        } else if (prev.hours > 0) {
          return { ...prev, hours: prev.hours - 1, minutes: 59, seconds: 59 };
        }
        return { hours: 24, minutes: 0, seconds: 0 };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar bgstate={true} />

      <main className="flex-1 w-full pt-20 sm:pt-24">
        {/* Urgent Promotional Announcement Bar */}
        <div className="w-full bg-red-600 text-white py-3 px-4 text-center">
          <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-6 text-xs sm:text-sm font-medium">
            <span>🔥 MID-SEASON ARCHIVE SALE: UP TO 30% OFF</span>
            <span className="hidden sm:inline">•</span>
            <div className="flex items-center gap-1.5 font-mono">
              <span>Ends in:</span>
              <span className="bg-black/30 px-2 py-0.5 rounded-xs">
                {String(timeLeft.hours).padStart(2, "0")}h
              </span>
              <span>:</span>
              <span className="bg-black/30 px-2 py-0.5 rounded-xs">
                {String(timeLeft.minutes).padStart(2, "0")}m
              </span>
              <span>:</span>
              <span className="bg-black/30 px-2 py-0.5 rounded-xs">
                {String(timeLeft.seconds).padStart(2, "0")}s
              </span>
            </div>
            <span className="hidden sm:inline">•</span>
            <span className="bg-white text-red-600 px-2.5 py-0.5 text-xs rounded-full font-bold uppercase">
              CODE: DROP10
            </span>
          </div>
        </div>

        {loading ? (
          <div className="w-full max-w-7xl mx-auto px-4 py-24 text-center">
            <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-neutral-500 text-sm">
              Loading sale archive from database...
            </p>
          </div>
        ) : (
          <CollectionGrid
            products={saleProducts}
            title="Seasonal Sale Drops"
            subtitle="Limited-run archival staples and seasonal favorites at exclusive marked-down prices."
            isSalePage={true}
            availableCategories={["All", "Tops", "Bottoms", "Outerwear"]}
          />
        )}
      </main>

      <Footer />
    </div>
  );
};

export default Sales;
