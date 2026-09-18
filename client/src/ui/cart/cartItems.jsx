import React from "react";
import { useNavigate } from "react-router-dom";
import useCart from "../../hooks/carts";
import { useToast } from "../../hooks/toast";

const CartItems = () => {
  const { cartItems, removeFromCart, updateQuantity, clearCart } = useCart();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const handleRemove = (index, itemName) => {
    removeFromCart(index);
    showToast(`Removed ${itemName} from cart`, "info");
  };

  return (
    <div className="flex flex-col w-full">
      <div className="flex items-center justify-between pb-4 border-b border-black/10">
        <h2 className="font-poppins font-medium text-lg sm:text-xl text-neutral-900">
          Bag ({cartItems.reduce((acc, item) => acc + item.quantity, 0)})
        </h2>
        {cartItems.length > 0 && (
          <button
            onClick={() => {
              clearCart();
              showToast("Cart cleared", "info");
            }}
            className="text-xs font-poppins text-neutral-500 hover:text-red-600 transition-colors underline cursor-pointer"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="divide-y divide-black/10">
        {cartItems.map((item, index) => {
          const numericPrice =
            parseFloat(
              String(item.price || "")
                .replace(/,/g, "")
                .replace(/[^0-9.]/g, ""),
            ) || 0;
          const lineTotal = (numericPrice * item.quantity).toFixed(2);

          return (
            <div
              key={`${item.item}-${item.selectedSize}-${index}`}
              className="py-6 flex flex-col sm:flex-row gap-4 sm:gap-6 items-start sm:items-center justify-between transition-all"
            >
              {/* Product Info with Image */}
              <div className="flex items-center gap-4 flex-1">
                <div
                  onClick={() =>
                    navigate("/product-description", {
                      state: { product: item },
                    })
                  }
                  className="w-20 sm:w-24 aspect-3/4 bg-neutral-100 shrink-0 overflow-hidden cursor-pointer"
                >
                  <img
                    src={item.image1}
                    alt={item.itemName}
                    className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  />
                </div>

                <div className="flex flex-col gap-1">
                  <h3
                    onClick={() =>
                      navigate("/product-description", {
                        state: { product: item },
                      })
                    }
                    className="font-poppins font-medium text-sm sm:text-base text-neutral-900 cursor-pointer hover:text-blue-600 transition-colors"
                  >
                    {item.itemName}
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-neutral-500 font-poppins">
                    <span>
                      Size:{" "}
                      <strong className="text-black uppercase">
                        {item.selectedSize || "Standard"}
                      </strong>
                    </span>
                    <span>•</span>
                    <span>Unit: {item.price}</span>
                  </div>
                  <span className="sm:hidden font-poppins font-semibold text-sm text-neutral-900 mt-1">
                    Rs. {lineTotal}
                  </span>
                </div>
              </div>

              {/* Quantity controls & Line Total */}
              <div className="flex items-center justify-between sm:justify-end gap-6 w-full sm:w-auto">
                {/* Quantity stepper */}
                <div className="flex items-center border border-black/20 rounded-xs">
                  <button
                    onClick={() => {
                      if (item.quantity > 1) {
                        updateQuantity(index, item.quantity - 1);
                      } else {
                        handleRemove(index, item.itemName);
                      }
                    }}
                    className="w-8 h-8 flex items-center justify-center text-sm hover:bg-neutral-100 transition-colors cursor-pointer"
                    aria-label="Decrease quantity"
                  >
                    −
                  </button>
                  <span className="w-9 text-center font-poppins text-xs sm:text-sm font-medium">
                    {item.quantity}
                  </span>
                  <button
                    onClick={() => updateQuantity(index, item.quantity + 1)}
                    className="w-8 h-8 flex items-center justify-center text-sm hover:bg-neutral-100 transition-colors cursor-pointer"
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>

                {/* Subtotal */}
                <div className="hidden sm:block text-right min-w-[70px]">
                  <span className="font-poppins font-semibold text-base text-neutral-900">
                    Rs. {lineTotal}
                  </span>
                </div>

                {/* Remove button */}
                <button
                  onClick={() => handleRemove(index, item.itemName)}
                  aria-label="Remove item"
                  className="w-8 h-8 flex items-center justify-center text-neutral-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors cursor-pointer"
                >
                  ✕
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CartItems;
