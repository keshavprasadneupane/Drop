import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import { CartItems, OrderSummary } from "../ui/cart/cartLayout";
import useCart from "../hooks/carts";
import { useToast } from "../hooks/toast";
import useAuth from "../hooks/auth";
import useBoughtProducts from "../hooks/boughtProducts";
import api from "../services/api";
import ProductCard from "../ui/collection/productCard";
import { getProducts } from "../services/productService";

const Carts = () => {
  const { cartItems, clearCart, getCartTotal } = useCart();
  const { addBoughtProducts } = useBoughtProducts();
  const { showToast } = useToast();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isOrderPlaced, setIsOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState("");
  const [checkoutTotal, setCheckoutTotal] = useState(0);
  const [trendingProducts, setTrendingProducts] = useState([]);

  const [checkoutData, setCheckoutData] = useState(() => ({
    fullName: user?.fullName || "",
    email: user?.email || "",
    address: "",
    city: "",
    postalCode: "",
    paymentMethod: "Credit Card",
  }));

  // Load trending recommendations from backend API for empty cart
  useEffect(() => {
    const loadTrending = async () => {
      try {
        const prods = await getProducts();
        if (prods && prods.length > 0) {
          setTrendingProducts(prods.slice(0, 4));
        }
      } catch (err) {
        console.error("Could not load recommendations:", err);
      }
    };
    loadTrending();
  }, []);

  const handleInputChange = (e) => {
    setCheckoutData({ ...checkoutData, [e.target.name]: e.target.value });
  };

  const handleOpenCheckout = (total) => {
    if (!isAuthenticated) {
      showToast(
        "Please log in with your account to proceed to payment.",
        "error",
      );
      navigate("/login?redirect=/carts");
      return;
    }
    if (user) {
      setCheckoutData((prev) => ({
        ...prev,
        fullName: prev.fullName || user.fullName || "",
        email: prev.email || user.email || "",
      }));
    }
    setCheckoutTotal(total || getCartTotal().toFixed(2));
    setIsCheckoutOpen(true);
  };

  const handleCheckoutSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated) {
      showToast("Authentication required to complete payment.", "error");
      navigate("/login?redirect=/carts");
      return;
    }

    setIsProcessing(true);

    try {
      const primaryItem = cartItems[0];
      const productCost = parseFloat(checkoutTotal) || getCartTotal();

      const paymentPayload = {
        product: primaryItem?.id || primaryItem?.item || null,
        product_name:
          cartItems
            .map((i) => i.itemName || i.itemname)
            .join(", ")
            .slice(0, 100) || "DROPP Fashion Order",
        cost: productCost,
        quantity: cartItems.reduce((acc, item) => acc + item.quantity, 0),
        fullname: checkoutData.fullName,
        email_address: checkoutData.email,
        shipping_address: checkoutData.address,
        city: checkoutData.city,
        postal_code: parseInt(checkoutData.postalCode) || 1000,
        payment_method: checkoutData.paymentMethod || "Credit Card",
      };

      const response = await api.post("/payment/post/", paymentPayload);

      // Check if Stripe Checkout session URL was provided
      if (
        response.data &&
        response.data.url &&
        response.data.url.includes("checkout.stripe.com")
      ) {
        showToast("Redirecting to secure Stripe Checkout...", "info");
        window.location.href = response.data.url;
        return;
      }

      // Successful order recording
      const returnedOrderId = response.data.payment_id
        ? `ORD-${response.data.payment_id + 100000}`
        : `ORD-${Math.floor(100000 + Math.random() * 900000)}`;

      // Save to bought products section & empty shopping bag
      addBoughtProducts(cartItems, {
        orderId: returnedOrderId,
        totalCost: productCost,
        paymentMethod: checkoutData.paymentMethod,
        shippingAddress: checkoutData.address,
      });

      setOrderId(returnedOrderId);
      setIsOrderPlaced(true);
      clearCart();
      showToast("Payment processed and order placed successfully!", "success");
    } catch (err) {
      const errorDetail =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Payment processing failed. Please try again.";
      showToast(errorDetail, "error");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins">
      <Navbar bgstate={true} />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 sm:pt-32 pb-16">
        <div className="flex items-center gap-2 text-xs sm:text-sm text-neutral-500 mb-6">
          <button
            onClick={() => navigate("/")}
            className="hover:text-black cursor-pointer"
          >
            Home
          </button>
          <span>/</span>
          <span className="text-black font-medium">Shopping Bag</span>
        </div>

        {cartItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 sm:py-20 text-center">
            <div className="w-20 h-20 rounded-full bg-neutral-100 flex items-center justify-center text-3xl mb-6">
              🛍️
            </div>
            <h1 className="font-poppins font-medium text-2xl sm:text-3xl text-neutral-900 mb-2">
              Your shopping bag is empty
            </h1>
            <p className="font-poppins font-light text-sm sm:text-base text-neutral-600 max-w-md mb-8">
              Looks like you haven't added anything to your bag yet. Discover
              our curated collections and upgrade your wardrobe.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={() => navigate("/women-collection")}
                className="bg-black text-white px-8 py-3 text-sm font-medium hover:bg-neutral-800 transition-all duration-300 cursor-pointer"
              >
                Shop Women
              </button>
              <button
                onClick={() => navigate("/men-collection")}
                className="bg-neutral-100 text-black px-8 py-3 text-sm font-medium hover:bg-neutral-200 transition-all duration-300 cursor-pointer"
              >
                Shop Men
              </button>
            </div>

            {trendingProducts.length > 0 && (
              <div className="w-full mt-20 text-left border-t border-black/10 pt-12">
                <h2 className="font-poppins font-medium text-xl text-neutral-900 mb-6">
                  Trending Right Now
                </h2>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6">
                  {trendingProducts.map((product) => (
                    <ProductCard
                      key={product.id || product.item}
                      product={product}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div>
            <div className="mb-8">
              <h1 className="font-poppins font-medium text-2xl sm:text-3xl lg:text-4xl text-neutral-900">
                Shopping Bag
              </h1>
              <p className="font-poppins font-light text-sm text-neutral-600 mt-1">
                Review your selected items and proceed to secure checkout.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
              <div className="lg:col-span-8">
                <CartItems />
              </div>

              <div className="lg:col-span-4 sticky top-28">
                <OrderSummary onCheckout={handleOpenCheckout} />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Authenticated Checkout Modal */}
      {isCheckoutOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-white w-full max-w-lg p-6 sm:p-8 rounded-sm shadow-2xl relative max-h-[90vh] overflow-y-auto">
            {!isOrderPlaced ? (
              <>
                <button
                  onClick={() => setIsCheckoutOpen(false)}
                  className="absolute top-4 right-4 text-neutral-400 hover:text-black text-lg cursor-pointer"
                  aria-label="Close modal"
                >
                  ✕
                </button>

                <div className="mb-6">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-green-700 bg-green-50 px-2 py-0.5 rounded-xs font-medium">
                      ✓ Authenticated Checkout
                    </span>
                  </div>
                  <h2 className="font-poppins font-medium text-xl sm:text-2xl text-neutral-900">
                    Express Checkout
                  </h2>
                  <p className="text-xs text-neutral-500 mt-1">
                    Total to pay:{" "}
                    <strong className="text-black">
                      Rs. {checkoutTotal || getCartTotal().toFixed(2)}
                    </strong>
                  </p>
                </div>

                <form
                  onSubmit={handleCheckoutSubmit}
                  className="flex flex-col gap-4"
                >
                  <div className="flex flex-col gap-1">
                    <label className="text-xs text-neutral-600 font-poppins">
                      Full Name
                    </label>
                    <input
                      type="text"
                      name="fullName"
                      required
                      placeholder="Jane Doe"
                      value={checkoutData.fullName}
                      onChange={handleInputChange}
                      className="border border-black/20 px-3 py-2 text-sm font-poppins focus:outline-none focus:border-black"
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-xs text-neutral-600 font-poppins">
                      Email Address
                    </label>
                    <input
                      type="email"
                      name="email"
                      required
                      placeholder="jane@example.com"
                      value={checkoutData.email}
                      onChange={handleInputChange}
                      className="border border-black/20 px-3 py-2 text-sm font-poppins focus:outline-none focus:border-black"
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-xs text-neutral-600 font-poppins">
                      Shipping Address
                    </label>
                    <input
                      type="text"
                      name="address"
                      required
                      placeholder="123 Fashion Blvd, Apt 4B"
                      value={checkoutData.address}
                      onChange={handleInputChange}
                      className="border border-black/20 px-3 py-2 text-sm font-poppins focus:outline-none focus:border-black"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="flex flex-col gap-1">
                      <label className="text-xs text-neutral-600 font-poppins">
                        City
                      </label>
                      <input
                        type="text"
                        name="city"
                        required
                        placeholder="Paris"
                        value={checkoutData.city}
                        onChange={handleInputChange}
                        className="border border-black/20 px-3 py-2 text-sm font-poppins focus:outline-none focus:border-black"
                      />
                    </div>
                    <div className="flex flex-col gap-1">
                      <label className="text-xs text-neutral-600 font-poppins">
                        Postal Code
                      </label>
                      <input
                        type="text"
                        name="postalCode"
                        required
                        placeholder="75001"
                        value={checkoutData.postalCode}
                        onChange={handleInputChange}
                        className="border border-black/20 px-3 py-2 text-sm font-poppins focus:outline-none focus:border-black"
                      />
                    </div>
                  </div>

                  <div className="flex flex-col gap-2 pt-2">
                    <label className="text-xs text-neutral-600 font-poppins">
                      Payment Method
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                      {["Credit Card", "eSewa", "Khalti"].map((method) => (
                        <button
                          type="button"
                          key={method}
                          onClick={() =>
                            setCheckoutData({
                              ...checkoutData,
                              paymentMethod: method,
                            })
                          }
                          className={`py-2 px-3 border text-xs font-poppins uppercase tracking-wider transition-colors cursor-pointer ${
                            checkoutData.paymentMethod === method
                              ? "border-black bg-black text-white"
                              : "border-black/20 text-neutral-700 hover:border-black"
                          }`}
                        >
                          {method}
                        </button>
                      ))}
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={isProcessing}
                    className="mt-4 bg-black text-white py-3.5 text-sm font-poppins font-medium hover:bg-neutral-800 transition-colors cursor-pointer flex items-center justify-center gap-2"
                  >
                    {isProcessing ? (
                      <span>Processing Authenticated Payment...</span>
                    ) : (
                      <span>
                        Confirm & Pay (Rs.{" "}
                        {checkoutTotal || getCartTotal().toFixed(2)})
                      </span>
                    )}
                  </button>
                </form>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <div className="w-16 h-16 rounded-full bg-green-100 text-green-600 text-3xl flex items-center justify-center mb-4">
                  ✓
                </div>
                <h2 className="font-poppins font-medium text-2xl text-neutral-900 mb-1">
                  Thank You for Your Order!
                </h2>
                <p className="text-xs text-neutral-500 mb-4">
                  Order reference:{" "}
                  <strong className="text-black">{orderId}</strong>
                </p>
                <p className="text-sm text-neutral-600 max-w-sm mb-6 font-light">
                  We've recorded your purchase and sent a confirmation email to{" "}
                  <strong className="font-medium text-black">
                    {checkoutData.email || user?.email || "your inbox"}
                  </strong>
                  .
                </p>
                <div className="flex flex-col sm:flex-row gap-3 w-full justify-center">
                  <button
                    onClick={() => {
                      setIsCheckoutOpen(false);
                      setIsOrderPlaced(false);
                      navigate("/bought-products");
                    }}
                    className="bg-black text-white px-6 py-3 text-sm font-poppins font-medium hover:bg-neutral-800 transition-colors cursor-pointer"
                  >
                    View Bought Products
                  </button>
                  <button
                    onClick={() => {
                      setIsCheckoutOpen(false);
                      setIsOrderPlaced(false);
                      navigate("/");
                    }}
                    className="border border-black text-black px-6 py-3 text-sm font-poppins font-medium hover:bg-neutral-100 transition-colors cursor-pointer"
                  >
                    Return to Home
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
};

export default Carts;
