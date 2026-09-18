import React, { useState, useEffect } from "react";
import { useLocation, useParams } from "react-router-dom";
import useCart from "../../hooks/carts";
import useFavs from "../../hooks/favs";
import { useToast } from "../../hooks/toast";
import {
  getProductById,
  normalizeProduct,
} from "../../services/productService";

const ProductDetails = () => {
  const location = useLocation();
  const params = useParams();
  const { addToCart } = useCart();
  const { toggleFavourite, isFavourite } = useFavs();
  const { showToast } = useToast();

  const [product, setProduct] = useState(() =>
    normalizeProduct(location.state?.product),
  );
  const [selectedImage, setSelectedImage] = useState(
    () => location.state?.product?.image1 || "",
  );
  const [selectedSize, setSelectedSize] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [sizeError, setSizeError] = useState(false);
  const [activeTab, setActiveTab] = useState("details"); // 'details' | 'shipping'
  const [loading, setLoading] = useState(!location.state?.product);

  const currentProductItem =
    location.state?.product?.item || location.state?.product?.id;
  const [prevProductItem, setPrevProductItem] = useState(currentProductItem);

  if (currentProductItem && currentProductItem !== prevProductItem) {
    setPrevProductItem(currentProductItem);
    const normalized = normalizeProduct(location.state.product);
    setProduct(normalized);
    setSelectedImage(normalized.image1);
    setSelectedSize(null);
    setQuantity(1);
    setSizeError(false);
  }

  useEffect(() => {
    if (location.state?.product) return;

    const targetId = params.id || 1;
    let isMounted = true;

    getProductById(targetId).then((data) => {
      if (isMounted && data) {
        setProduct(data);
        setSelectedImage(data.image1);
        setSelectedSize(null);
        setQuantity(1);
        setSizeError(false);
      }
      if (isMounted) setLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [location.state?.product, params.id]);

  const isFav = product ? isFavourite(product) : false;

  const handleAddToCart = () => {
    if (!product) return;
    if (!selectedSize) {
      setSizeError(true);
      showToast("Please choose a size to continue", "error");
      return;
    }
    setSizeError(false);
    addToCart(product, selectedSize, quantity);
    showToast(
      `Added ${quantity} × ${product.itemName} (${selectedSize}) to bag!`,
      "success",
    );
  };

  const handleToggleFav = () => {
    if (!product) return;
    toggleFavourite(product);
    if (isFav) {
      showToast("Removed from favourites", "info");
    } else {
      showToast("Added to favourites ♥", "success");
    }
  };

  if (loading || !product) {
    return (
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center">
        <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-neutral-500 text-sm">
          Loading product details from database...
        </p>
      </div>
    );
  }

  const {
    itemName,
    description,
    image1,
    image2,
    price,
    ratings,
    availableSizes = ["XS", "S", "M", "L", "XL"],
    details_and_care = [],
    shipping_and_return = [],
  } = product;

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-16 items-start">
        {/* Left: Product Images Gallery */}
        <div className="lg:col-span-7 flex flex-col-reverse sm:flex-row gap-4">
          {/* Thumbnails */}
          <div className="flex sm:flex-col gap-3 shrink-0 overflow-x-auto sm:overflow-visible">
            {[image1, image2].filter(Boolean).map((img, index) => (
              <button
                key={index}
                onClick={() => setSelectedImage(img)}
                className={`w-16 sm:w-20 aspect-3/4 overflow-hidden border transition-all cursor-pointer bg-neutral-100 ${
                  selectedImage === img
                    ? "border-black ring-1 ring-black"
                    : "border-black/10 hover:border-black/40"
                }`}
              >
                <img
                  src={img}
                  alt={`${itemName} angle ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </button>
            ))}
          </div>

          {/* Main Hero Image */}
          <div className="flex-1 aspect-3/4 max-h-[640px] bg-neutral-100 overflow-hidden relative group">
            <img
              src={selectedImage || image1}
              alt={itemName}
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <span className="absolute top-4 right-4 bg-white/90 backdrop-blur-xs text-xs font-poppins px-2.5 py-1 text-neutral-800 shadow-xs">
              ★ {ratings}
            </span>
          </div>
        </div>

        {/* Right: Product Details & Purchase Form */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* Header */}
          <div className="flex flex-col gap-2 border-b border-black/10 pb-6">
            <span className="text-xs uppercase tracking-widest text-neutral-400 font-medium">
              DROPP ESSENTIALS
            </span>
            <h1 className="font-poppins font-medium text-2xl sm:text-3xl text-neutral-900 leading-tight">
              {itemName}
            </h1>
            <div className="flex items-center gap-3 mt-1">
              <span className="font-poppins font-semibold text-xl text-neutral-900">
                {price}
              </span>
              <span className="text-xs text-green-700 bg-green-50 px-2 py-0.5 rounded-xs font-medium">
                In Stock & Ready to Ship
              </span>
            </div>
          </div>

          {/* Description */}
          <p className="font-poppins font-light text-sm text-neutral-600 leading-relaxed">
            {description}
          </p>

          {/* Size Selection */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center justify-between text-xs font-poppins">
              <span className="font-medium text-neutral-900">
                Select Size:{" "}
                {selectedSize ? (
                  <strong className="text-black uppercase">
                    {selectedSize}
                  </strong>
                ) : (
                  <span className="text-neutral-400 font-normal">
                    Choose one
                  </span>
                )}
              </span>
              <button
                type="button"
                onClick={() =>
                  showToast(
                    "Sizes fit true-to-size with a relaxed drape.",
                    "info",
                  )
                }
                className="text-neutral-500 underline hover:text-black cursor-pointer"
              >
                Size Guide
              </button>
            </div>

            <div className="flex flex-wrap gap-2">
              {availableSizes.map((size) => (
                <button
                  key={size}
                  onClick={() => {
                    setSelectedSize(size);
                    setSizeError(false);
                  }}
                  className={`min-w-[48px] h-12 px-3 border font-poppins text-xs font-medium cursor-pointer transition-all duration-200 ${
                    selectedSize === size
                      ? "border-black bg-black text-white shadow-xs"
                      : "border-black/20 text-neutral-800 hover:border-black bg-white"
                  }`}
                >
                  {size}
                </button>
              ))}
            </div>

            {sizeError && (
              <span className="text-xs text-red-600 font-poppins">
                ⚠️ Please select your size before adding to bag
              </span>
            )}
          </div>

          {/* Quantity selector */}
          <div className="flex items-center gap-4">
            <span className="text-xs font-poppins text-neutral-600">
              Quantity:
            </span>
            <div className="flex items-center border border-black/20 rounded-xs">
              <button
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                className="w-9 h-9 flex items-center justify-center text-sm hover:bg-neutral-100 transition-colors cursor-pointer"
              >
                −
              </button>
              <span className="w-10 text-center font-poppins text-sm font-medium">
                {quantity}
              </span>
              <button
                onClick={() => setQuantity((q) => q + 1)}
                className="w-9 h-9 flex items-center justify-center text-sm hover:bg-neutral-100 transition-colors cursor-pointer"
              >
                +
              </button>
            </div>
          </div>

          {/* Actions: Add to Bag & Wishlist */}
          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <button
              onClick={handleAddToCart}
              className="flex-1 bg-black text-white font-poppins font-medium text-sm py-4 px-6 hover:bg-neutral-800 transition-all duration-300 cursor-pointer shadow-sm hover:-translate-y-0.5"
            >
              Add to Bag • {price}
            </button>
            <button
              onClick={handleToggleFav}
              className={`sm:w-16 h-12 sm:h-auto border font-poppins text-sm transition-all duration-300 cursor-pointer flex items-center justify-center gap-2 ${
                isFav
                  ? "border-red-600 bg-red-50 text-red-600"
                  : "border-black/20 text-neutral-800 hover:border-black hover:bg-neutral-50"
              }`}
              title={isFav ? "Saved in favourites" : "Save to favourites"}
            >
              <span className="text-base">{isFav ? "♥" : "♡"}</span>
              <span className="sm:hidden text-xs">
                {isFav ? "Saved" : "Save to Favourites"}
              </span>
            </button>
          </div>

          {/* Accordion tabs for Details / Shipping */}
          <div className="border-t border-black/10 pt-6 mt-2 flex flex-col gap-4">
            <div className="flex gap-6 border-b border-black/10">
              <button
                onClick={() => setActiveTab("details")}
                className={`pb-2 text-xs uppercase font-poppins tracking-wider cursor-pointer transition-colors ${
                  activeTab === "details"
                    ? "border-b-2 border-black font-semibold text-black"
                    : "text-neutral-400 hover:text-neutral-700"
                }`}
              >
                Details & Care
              </button>
              <button
                onClick={() => setActiveTab("shipping")}
                className={`pb-2 text-xs uppercase font-poppins tracking-wider cursor-pointer transition-colors ${
                  activeTab === "shipping"
                    ? "border-b-2 border-black font-semibold text-black"
                    : "text-neutral-400 hover:text-neutral-700"
                }`}
              >
                Shipping & Returns
              </button>
            </div>

            <div className="text-xs text-neutral-600 font-poppins leading-relaxed">
              {activeTab === "details" ? (
                <ul className="space-y-1.5 list-disc list-inside">
                  {details_and_care.length > 0 ? (
                    details_and_care.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))
                  ) : (
                    <>
                      <li>100% Ring-spun heavyweight combed cotton</li>
                      <li>Preshrunk fabric to minimize shrinkage</li>
                      <li>
                        Reinforced twin-needle stitching at collar and cuffs
                      </li>
                      <li>
                        Machine wash cold inside-out, hang dry recommended
                      </li>
                    </>
                  )}
                </ul>
              ) : (
                <div className="space-y-1.5">
                  {shipping_and_return.length > 0 ? (
                    shipping_and_return.map((item, idx) => (
                      <p key={idx}>• {item}</p>
                    ))
                  ) : (
                    <>
                      <p>
                        • Complimentary standard shipping on all orders over Rs.
                        5,000.
                      </p>
                      <p>• Hassle-free 30-day returns and exchanges.</p>
                      <p>• Estimated delivery: 2-4 business days.</p>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
