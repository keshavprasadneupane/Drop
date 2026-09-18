import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useCart from "../hooks/carts";
import useBoughtProducts from "../hooks/boughtProducts";

const SuccessPayment = () => {
  const navigate = useNavigate();
  const { cartItems, clearCart } = useCart();
  const { addBoughtProducts, fetchMyPayments } = useBoughtProducts();

  useEffect(() => {
    if (cartItems && cartItems.length > 0) {
      addBoughtProducts(cartItems, { paymentMethod: "Stripe Checkout" });
      clearCart();
    }
    fetchMyPayments();
  }, []);

  return (
    <div className="flex bg-black w-full min-h-screen items-center justify-center flex-col px-4 text-center">
      <div className="w-20 h-20 rounded-full bg-green-500/20 text-green-400 flex items-center justify-center text-4xl mb-6">
        ✓
      </div>
      <h1 className="font-poppins font-bold text-white text-4xl sm:text-6xl mb-4">
        Payment Received :)
      </h1>
      <p className="font-poppins font-light text-white/60 max-w-md">
        Your payment was processed successfully. A confirmation receipt has been
        dispatched to your email address.
      </p>

      <div className="flex flex-col sm:flex-row gap-4 mt-10">
        <button
          onClick={() => navigate("/bought-products")}
          className="bg-white text-black py-3.5 px-8 font-poppins font-medium cursor-pointer hover:bg-neutral-200 transition-all duration-300"
        >
          View Bought Products
        </button>
        <button
          onClick={() => navigate("/")}
          className="border border-white py-3.5 px-8 text-white font-poppins font-medium cursor-pointer hover:bg-white hover:text-black transition-all duration-300"
        >
          Take me to Home Screen
        </button>
      </div>
    </div>
  );
};

export default SuccessPayment;
