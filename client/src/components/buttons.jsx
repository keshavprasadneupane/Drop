import { useNavigate } from "react-router-dom";
import useCart from "../hooks/carts";
import useFavs from "../hooks/favs";
import { useToast } from "../hooks/toast";

export const AuthButton = ({ buttonName, navigateTo }) => {
  const navigate = useNavigate();
  return (
    <button
      onClick={() => navigate(navigateTo)}
      className="flex border font-poppins border-white px-3 sm:px-large py-2 sm:py-small text-xs sm:text-sm text-white whitespace-nowrap cursor-pointer transition-all duration-300 ease-out hover:bg-white hover:text-black hover:-translate-y-0.5 items-center justify-center w-full"
    >
      {buttonName}
    </button>
  );
};

export const PrimaryButton = ({ buttonName, navigateTo }) => {
  const navigate = useNavigate();
  return (
    <button
      onClick={() => navigate(navigateTo)}
      className="flex justify-center font-poppins bg-white px-6 sm:px-extralarge py-3 sm:py-mid text-sm sm:text-base text-black whitespace-nowrap cursor-pointer transition-all duration-300 ease-out hover:bg-black hover:text-white hover:-translate-y-0.5 w-full sm:w-auto"
    >
      {buttonName}
    </button>
  );
};

export const PrimaryBlackButton = ({ buttonName, navigateTo, onClick }) => {
  const navigate = useNavigate();
  return (
    <button
      onClick={onClick ? onClick : () => navigate(navigateTo)}
      className="flex lg:px-8 lg:py-4 justify-center font-poppins bg-black px-6 sm:px-extralarge py-3 sm:py-mid text-sm sm:text-base text-white whitespace-nowrap cursor-pointer transition-all duration-300 ease-out hover:bg-amber-400 hover:text-white hover:-translate-y-0.5 w-full sm:w-auto"
    >
      {buttonName}
    </button>
  );
};

export const AddtoFavButton = ({ data }) => {
  const { toggleFavourite, isFavourite } = useFavs();
  const { showToast } = useToast();
  const isFav = isFavourite(data);

  const handleAction = () => {
    toggleFavourite(data);
    if (isFav) {
      showToast("Removed from favourites", "info");
    } else {
      showToast("Added to favourites ♥", "success");
    }
  };

  return (
    <button
      onClick={handleAction}
      className={`flex lg:px-8 lg:py-4 justify-center font-poppins px-6 sm:px-extralarge py-3 sm:py-mid text-sm sm:text-base whitespace-nowrap cursor-pointer transition-all duration-300 ease-out hover:-translate-y-0.5 w-full sm:w-auto ${
        isFav
          ? "bg-red-600 text-white hover:bg-red-700"
          : "bg-black text-white hover:bg-amber-400"
      }`}
    >
      {isFav ? "♥ Saved" : "♡ Add to Fav"}
    </button>
  );
};

export const CartButton = ({ navigateTo }) => {
  const { getCartCount } = useCart();
  const navigate = useNavigate();
  const count = getCartCount();
  return (
    <button
      onClick={() => navigate(navigateTo || "/carts")}
      className={`flex font-poppins ${
        count > 0 ? "bg-primaryred" : "bg-amber-400"
      } px-3 sm:px-large py-2 sm:py-small text-xs sm:text-sm text-white whitespace-nowrap cursor-pointer transition-all duration-300 ease-out hover:bg-primaryred hover:text-white hover:-translate-y-0.5`}
    >
      CART: {count}
    </button>
  );
};

export const AddToCartButton = ({ product, selectedSize, onRequireSize }) => {
  const { addToCart } = useCart();
  const { showToast } = useToast();

  const handleAddToCart = () => {
    if (!selectedSize) {
      if (onRequireSize) onRequireSize();
      return;
    }
    addToCart(product, selectedSize);
    showToast(`Added to cart — ${selectedSize}`, "success");
  };

  return (
    <button
      onClick={handleAddToCart}
      className="flex font-poppins bg-amber-400
      lg:px-8 sm:px-large w-full lg:py-4 sm:py-small text-xs sm:text-sm text-white whitespace-nowrap cursor-pointer transition-all duration-300 ease-out hover:bg-black hover:text-white hover:-translate-y-0.5 items-center justify-center"
    >
      Add to Cart
    </button>
  );
};
