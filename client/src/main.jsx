import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { AuthProvider } from "./hooks/auth";
import { CartProvider } from "./hooks/carts";
import { FavouritesProvider } from "./hooks/favs";
import { ToastProvider } from "./hooks/toast";
import { BoughtProductsProvider } from "./hooks/boughtProducts";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ToastProvider>
      <AuthProvider>
        <CartProvider>
          <FavouritesProvider>
            <BoughtProductsProvider>
              <App />
            </BoughtProductsProvider>
          </FavouritesProvider>
        </CartProvider>
      </AuthProvider>
    </ToastProvider>
  </StrictMode>,
);
