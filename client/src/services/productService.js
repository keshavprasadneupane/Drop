import api from "./api";
import { Data } from "../utils/clothesProductsData";
import { CustomerReviews as fallbackReviews } from "../utils/customerReview";

export const normalizeProduct = (p) => {
  if (!p) return null;
  const images =
    Array.isArray(p.images) && p.images.length > 0
      ? p.images
      : [p.image1, p.image2].filter(Boolean);

  const image1 = p.image1 || images[0] || "";
  const image2 = p.image2 || images[1] || images[0] || "";
  let price = p.price;
  if (typeof price === "number") {
    price = `Rs. ${price.toLocaleString()}`;
  } else if (!price) {
    price = "Rs. 0";
  } else if (!price.startsWith("Rs.") && !price.startsWith("NPR")) {
    const cleanNumber = String(price)
      .replace(/,/g, "")
      .replace(/[^0-9.]/g, "");
    price = `Rs. ${cleanNumber || 0}`;
  }
  const availableSizes = p.available_sizes ||
    p.availableSizes || ["XS", "S", "M", "L", "XL"];

  return {
    id: p.id || p.item,
    item: p.id || p.item,
    itemName: p.itemname || p.itemName,
    itemname: p.itemname || p.itemName,
    description: p.description || "",
    image1,
    image2,
    images: images.length > 0 ? images : [image1, image2],
    price,
    ratings: p.ratings || "4.8",
    availableSizes,
    available_sizes: availableSizes,
    gender: p.gender || "unisex",
    details_and_care: p.details_and_care || [],
    shipping_and_return: p.shipping_and_return || [],
  };
};

// Fetch all products with optional gender filter from FastAPI backend
export const getProducts = async (gender = null) => {
  try {
    const params = {};
    if (gender) params.gender = gender;
    const response = await api.get("/products/list-all-products/", { params });
    const rawList = response.data?.data || [];
    if (rawList.length > 0) {
      return rawList.map(normalizeProduct);
    }
  } catch (err) {
    console.warn(
      "Could not fetch products from API, using fallback data:",
      err,
    );
  }

  // Fallback to local data
  const women = (Data[0]?.women || []).map((p) =>
    normalizeProduct({ ...p, gender: "female" }),
  );
  const men = (Data[0]?.men || []).map((p) =>
    normalizeProduct({ ...p, gender: "male" }),
  );

  if (gender === "female") return women;
  if (gender === "male") return men;
  return [...women, ...men];
};

// Fetch single product by ID from FastAPI backend
export const getProductById = async (productId) => {
  try {
    const response = await api.get(`/products/${productId}/`);
    if (response.data?.data) {
      return normalizeProduct(response.data.data);
    }
  } catch (err) {
    console.warn(`Could not fetch product ${productId} from API:`, err);
  }

  // Fallback to local dataset
  const all = [...(Data[0]?.women || []), ...(Data[0]?.men || [])];
  const match = all.find(
    (p) =>
      String(p.item) === String(productId) ||
      String(p.id) === String(productId),
  );
  return match ? normalizeProduct(match) : null;
};

// Fetch customer reviews from FastAPI backend
export const getCustomerReviews = async (productId = null) => {
  try {
    const url = productId
      ? `/review/product/${productId}/`
      : "/review/list-all-review/";
    const response = await api.get(url);
    const rawReviews = response.data?.data || [];
    if (rawReviews.length > 0) {
      return rawReviews.map((r) => ({
        id: r.id,
        customerName: r.customer_name || "Verified Customer",
        rating: r.customer_rating || 5,
        review: r.customer_review || "",
        date: r.review_timing
          ? new Date(r.review_timing).toLocaleDateString()
          : "Recent review",
        productName: r.product ? `Product #${r.product}` : "Verified Purchase",
      }));
    }
  } catch (err) {
    console.warn(
      "Could not fetch reviews from API, using fallback reviews:",
      err,
    );
  }

  return fallbackReviews;
};
