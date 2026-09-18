import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import useCart from "../../hooks/carts";
import { useToast } from "../../hooks/toast";
import useAuth from "../../hooks/auth";

const OrderSummary = ({ onCheckout }) => {
  const { getCartTotal, cartItems } = useCart();
  const { showToast } = useToast();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [promoCode, setPromoCode] = useState("");
  const [appliedDiscount, setAppliedDiscount] = useState(0);
  const [promoError, setPromoError] = useState("");
  const [promoSuccess, setPromoSuccess] = useState("");

  const subtotal = getCartTotal();
  const isFreeShipping =
    subtotal >= 5000 || promoSuccess.includes("Free shipping");
  const shippingCost = subtotal > 0 && !isFreeShipping ? 150 : 0;
  const discountAmount = (subtotal * appliedDiscount) / 100;
  const total = Math.max(0, subtotal - discountAmount + shippingCost).toFixed(
    2,
  );

  const handleApplyPromo = (e) => {
    e.preventDefault();
    setPromoError("");
    setPromoSuccess("");

    const code = promoCode.trim().toUpperCase();
    if (!code) return;

    if (code === "DROP10") {
      setAppliedDiscount(10);
      setPromoSuccess("10% discount applied!");
      showToast("Coupon applied: 10% OFF", "success");
    } else if (code === "DROP20") {
      setAppliedDiscount(20);
      setPromoSuccess("20% VIP discount applied!");
      showToast("Coupon applied: 20% OFF", "success");
    } else if (code === "FREESHIP") {
      setPromoSuccess("Free shipping unlocked!");
      showToast("Free shipping applied!", "success");
    } else {
      setPromoError("Invalid promo code. Try 'DROP10' or 'FREESHIP'");
    }
  };

  const handleCheckoutClick = () => {
    if (cartItems.length === 0) return;

    if (!isAuthenticated) {
      showToast(
        "Please log in with your account to proceed to payment.",
        "error",
      );
      navigate("/login?redirect=/carts");
      return;
    }

    onCheckout(total);
  };

  return (
    <div className="w-full bg-neutral-50 p-6 sm:p-8 border border-black/10 flex flex-col gap-6 font-poppins">
      <h2 className="font-medium text-lg sm:text-xl text-neutral-900 border-b border-black/10 pb-4">
        Order Summary
      </h2>

      {/* Breakdown */}
      <div className="flex flex-col gap-3 text-sm">
        <div className="flex items-center justify-between text-neutral-600">
          <span>Subtotal</span>
          <span className="text-neutral-900 font-medium">
            Rs. {subtotal.toLocaleString()}
          </span>
        </div>

        <div className="flex items-center justify-between text-neutral-600">
          <div className="flex items-center gap-1.5">
            <span>Shipping</span>
            <span className="text-[11px] text-neutral-400">
              {subtotal < 5000 ? `(Free over Rs. 5,000)` : `(Standard)`}
            </span>
          </div>
          <span className="text-neutral-900 font-medium">
            {isFreeShipping ? (
              <span className="text-green-600 font-semibold uppercase text-xs">
                Free
              </span>
            ) : (
              `Rs. ${shippingCost}`
            )}
          </span>
        </div>

        {appliedDiscount > 0 && (
          <div className="flex items-center justify-between text-green-600">
            <span>Discount ({appliedDiscount}%)</span>
            <span>-Rs. {discountAmount.toFixed(2)}</span>
          </div>
        )}

        <div className="border-t border-black/10 pt-4 mt-1 flex items-center justify-between font-medium text-base sm:text-lg text-neutral-900">
          <span>Total</span>
          <span>Rs. {total}</span>
        </div>
      </div>

      {/* Promo Code Form */}
      <form onSubmit={handleApplyPromo} className="flex flex-col gap-2">
        <div className="flex gap-2">
          <input
            type="text"
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value)}
            placeholder="Promo code (e.g. DROP10)"
            className="flex-1 bg-white border border-black/20 px-3 py-2 text-xs font-poppins text-neutral-900 placeholder:text-neutral-400 focus:outline-none focus:border-black uppercase"
          />
          <button
            type="submit"
            className="bg-black text-white text-xs font-poppins px-4 py-2 hover:bg-neutral-800 transition-colors cursor-pointer"
          >
            Apply
          </button>
        </div>
        {promoSuccess && (
          <span className="text-xs text-green-600 font-poppins">
            ✓ {promoSuccess}
          </span>
        )}
        {promoError && (
          <span className="text-xs text-red-600 font-poppins">
            {promoError}
          </span>
        )}
      </form>

      {/* Checkout Button */}
      <button
        onClick={handleCheckoutClick}
        disabled={cartItems.length === 0}
        className="w-full bg-black text-white py-3.5 px-6 font-poppins font-medium text-sm tracking-wide transition-all duration-300 hover:bg-neutral-800 hover:-translate-y-0.5 active:translate-y-0 disabled:bg-neutral-300 disabled:cursor-not-allowed cursor-pointer flex items-center justify-center gap-2 shadow-sm"
      >
        <span>
          {isAuthenticated ? "Proceed to Checkout" : "Log In to Checkout"}
        </span>
        <span>→</span>
      </button>

      {/* Trust & Guarantee */}
      <div className="border-t border-black/10 pt-4 flex flex-col gap-2 text-xs text-neutral-500 font-poppins">
        <div className="flex items-center gap-2">
          <span>✓</span>
          <span>Free 30-day returns on all orders</span>
        </div>
        <div className="flex items-center gap-2">
          <span>🔒</span>
          <span>Secure checkout with user authentication</span>
        </div>
        <div className="flex items-center gap-2">
          <span>⚡</span>
          <span>Dispatched within 24-48 business hours</span>
        </div>
      </div>
    </div>
  );
};

export default OrderSummary;
