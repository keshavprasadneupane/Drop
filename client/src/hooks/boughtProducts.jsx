import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import api from "../services/api";

const BoughtProductsContext = createContext(null);

const getInitialBought = () => {
  try {
    const stored = localStorage.getItem("dropp_bought_products");
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

export const BoughtProductsProvider = ({ children }) => {
  const [boughtItems, setBoughtItems] = useState(getInitialBought);
  const [isLoading, setIsLoading] = useState(false);

  // Sync to localStorage
  useEffect(() => {
    localStorage.setItem("dropp_bought_products", JSON.stringify(boughtItems));
  }, [boughtItems]);

  // Fetch from backend API if authenticated
  const fetchMyPayments = useCallback(async () => {
    const token = localStorage.getItem("dropp_access_token");
    if (!token) return;

    setIsLoading(true);
    try {
      const res = await api.get("/payment/my-payments/");
      if (res.data && res.data.data) {
        const remotePayments = res.data.data;
        // Merge remote payments if any
        setBoughtItems((prevLocal) => {
          const localMap = new Map(
            prevLocal.map((i) => [i.orderId || i.id, i]),
          );

          remotePayments.forEach((p) => {
            const orderKey = `ORD-${p.id + 100000}`;
            if (!localMap.has(orderKey) && !localMap.has(p.id)) {
              localMap.set(orderKey, {
                id: p.id,
                orderId: orderKey,
                itemName: p.product_name || "DROPP Product",
                price: `Rs. ${p.cost}`,
                selectedSize: "Standard",
                quantity: p.quantity || 1,
                images: [],
                purchaseDate: new Date().toISOString(),
                paymentMethod: p.payment_method || "Credit Card",
                shippingAddress: p.shipping_address || "",
              });
            }
          });
          return Array.from(localMap.values());
        });
      }
    } catch (err) {
      console.error("Could not fetch remote payments:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMyPayments();
  }, [fetchMyPayments]);

  const addBoughtProducts = useCallback((items, orderDetails = {}) => {
    if (!items || items.length === 0) return;

    const formattedDate = new Date().toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });

    const newBoughtEntries = items.map((item, index) => ({
      uniqueId: `${Date.now()}-${index}-${Math.random().toString(36).substr(2, 4)}`,
      id: item.id || item.item || index,
      orderId:
        orderDetails.orderId ||
        `ORD-${Math.floor(100000 + Math.random() * 900000)}`,
      itemName: item.itemName || item.itemname || "DROPP Exclusive Item",
      price: item.price || `Rs. ${orderDetails.totalCost || 0}`,
      selectedSize: item.selectedSize || "Standard",
      quantity: item.quantity || 1,
      images:
        item.images || item.image
          ? Array.isArray(item.images)
            ? item.images
            : [item.image]
          : [],
      purchaseDate: formattedDate,
      timestamp: Date.now(),
      paymentMethod: orderDetails.paymentMethod || "Credit Card",
      shippingAddress: orderDetails.shippingAddress || "",
    }));

    setBoughtItems((prev) => [...newBoughtEntries, ...prev]);
  }, []);

  const clearBoughtHistory = useCallback(() => {
    setBoughtItems([]);
    localStorage.removeItem("dropp_bought_products");
  }, []);

  return (
    <BoughtProductsContext.Provider
      value={{
        boughtItems,
        addBoughtProducts,
        clearBoughtHistory,
        fetchMyPayments,
        isLoading,
      }}
    >
      {children}
    </BoughtProductsContext.Provider>
  );
};

export const useBoughtProducts = () => {
  const context = useContext(BoughtProductsContext);
  if (!context) {
    throw new Error(
      "useBoughtProducts must be used within a BoughtProductsProvider",
    );
  }
  return context;
};

export default useBoughtProducts;
