import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import useBoughtProducts from "../hooks/boughtProducts";

const BoughtProducts = () => {
  const { boughtItems, clearBoughtHistory } = useBoughtProducts();
  const navigate = useNavigate();

  const getImageUrl = (images) => {
    if (!images) return null;
    if (Array.isArray(images) && images.length > 0) return images[0];
    if (typeof images === "string") return images;
    return null;
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar bgstate={true} />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 sm:pt-32 pb-16">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-xs sm:text-sm text-neutral-500 mb-6">
          <button
            onClick={() => navigate("/")}
            className="hover:text-black cursor-pointer"
          >
            Home
          </button>
          <span>/</span>
          <span className="text-black font-medium">Bought Products</span>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="font-poppins font-medium text-2xl sm:text-3xl lg:text-4xl text-neutral-900">
              Bought Products
            </h1>
            <p className="font-poppins font-light text-sm text-neutral-600 mt-1">
              Your confirmed purchases and order details.
            </p>
          </div>

          {boughtItems.length > 0 && (
            <button
              onClick={clearBoughtHistory}
              className="self-start sm:self-auto text-xs text-neutral-400 hover:text-red-500 underline cursor-pointer transition-colors"
            >
              Clear Purchase History
            </button>
          )}
        </div>

        {boughtItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center bg-neutral-50 rounded-sm border border-neutral-100 p-8">
            <div className="w-20 h-20 rounded-full bg-neutral-200/60 flex items-center justify-center text-3xl mb-6">
              📦
            </div>
            <h2 className="font-poppins font-medium text-2xl text-neutral-900 mb-2">
              No bought products yet
            </h2>
            <p className="font-poppins font-light text-sm text-neutral-600 max-w-md mb-8">
              Items you purchase will automatically appear here right after
              checkout.
            </p>
            <button
              onClick={() => navigate("/collection")}
              className="bg-black text-white px-8 py-3.5 text-sm font-medium hover:bg-neutral-800 transition-all duration-300 cursor-pointer"
            >
              Explore Collection
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {boughtItems.map((item, index) => {
              const img = getImageUrl(item.images);
              return (
                <div
                  key={item.uniqueId || index}
                  className="flex flex-col sm:flex-row items-start sm:items-center justify-between bg-white border border-neutral-200 p-5 sm:p-6 rounded-sm shadow-xs hover:border-black/30 transition-all duration-300 gap-6"
                >
                  <div className="flex items-center gap-4 sm:gap-6 w-full sm:w-auto">
                    <div className="w-20 h-24 sm:w-24 sm:h-28 bg-neutral-100 flex-shrink-0 rounded-xs overflow-hidden relative border border-neutral-200">
                      {img ? (
                        <img
                          src={img}
                          alt={item.itemName}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-xs text-neutral-400 font-mono">
                          DROPP
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col gap-1.5 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-xs">
                          ✓ Purchased
                        </span>
                        <span className="text-xs text-neutral-400 font-mono">
                          {item.orderId}
                        </span>
                      </div>

                      <h3 className="font-poppins font-medium text-base sm:text-lg text-neutral-900 leading-snug">
                        {item.itemName}
                      </h3>

                      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-neutral-600">
                        {item.selectedSize && (
                          <span>
                            Size:{" "}
                            <strong className="text-neutral-900">
                              {item.selectedSize}
                            </strong>
                          </span>
                        )}
                        <span>
                          Qty:{" "}
                          <strong className="text-neutral-900">
                            {item.quantity}
                          </strong>
                        </span>
                        {item.purchaseDate && (
                          <span>
                            Date:{" "}
                            <strong className="text-neutral-900">
                              {item.purchaseDate}
                            </strong>
                          </span>
                        )}
                      </div>

                      {item.paymentMethod && (
                        <span className="text-xs text-neutral-400">
                          Paid via {item.paymentMethod}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex sm:flex-col items-center sm:items-end justify-between w-full sm:w-auto border-t sm:border-t-0 pt-4 sm:pt-0 border-neutral-100 gap-2">
                    <span className="font-poppins font-semibold text-lg sm:text-xl text-neutral-900">
                      {item.price}
                    </span>
                    <button
                      onClick={() => navigate("/collection")}
                      className="text-xs bg-neutral-100 hover:bg-black hover:text-white px-4 py-2 font-medium transition-colors duration-300 cursor-pointer"
                    >
                      Buy Again
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
};

export default BoughtProducts;
