import React, { useState, useEffect } from "react";
import { getCustomerReviews } from "../../services/productService";

const CustomerReview = ({ productId = null }) => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const loadReviews = async () => {
      try {
        const data = await getCustomerReviews(productId);
        if (isMounted) setReviews(data);
      } catch (err) {
        console.error("Failed to load customer reviews:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    loadReviews();
    return () => {
      isMounted = false;
    };
  }, [productId]);

  return (
    <section className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 border-t border-black/10 font-poppins">
      <div className="flex flex-col gap-1 mb-8">
        <h2 className="font-medium text-xl sm:text-2xl text-neutral-900">
          Customer Reviews
        </h2>
        <p className="text-xs sm:text-sm text-neutral-500">
          Verified community experiences from database
        </p>
      </div>

      {loading ? (
        <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
          {Array(3)
            .fill(0)
            .map((_, i) => (
              <div
                key={i}
                className="shrink-0 w-72 sm:w-84 border border-black/10 p-5 bg-neutral-50 animate-pulse h-40"
              />
            ))}
        </div>
      ) : reviews.length === 0 ? (
        <p className="text-xs text-neutral-500 italic">
          No reviews yet. Be the first to review!
        </p>
      ) : (
        <div className="flex flex-row gap-4 overflow-x-auto pb-4 scrollbar-hide">
          {reviews.map((review) => (
            <div
              key={review.id}
              className="flex flex-col shrink-0 w-72 sm:w-84 border border-black/10 p-5 bg-white justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex flex-col">
                    <h3 className="font-medium text-sm text-neutral-900">
                      {review.customerName}
                    </h3>
                    <span className="text-[11px] text-neutral-400">
                      {review.date}
                    </span>
                  </div>
                  <div className="flex text-amber-500 text-xs">
                    {"★".repeat(Math.min(5, Math.max(1, review.rating || 5)))}
                  </div>
                </div>

                <p className="text-xs sm:text-sm text-neutral-600 leading-relaxed italic">
                  "{review.review}"
                </p>
              </div>

              <div className="pt-4 mt-4 border-t border-black/5 text-[11px] text-neutral-400">
                Purchased:{" "}
                <strong className="text-neutral-700 font-medium">
                  {review.productName}
                </strong>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default CustomerReview;
