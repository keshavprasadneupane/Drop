import React from "react";
import { useNavigate } from "react-router-dom";

const FailedPayment = () => {
  const navigate = useNavigate();
  return (
    <div className="flex bg-black w-full min-h-screen items-center justify-center flex-col px-4 text-center">
      <div className="w-20 h-20 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center text-4xl mb-6">
        ✕
      </div>
      <h1 className="font-poppins font-bold text-white text-4xl sm:text-6xl mb-4">
        Payment Incomplete :(
      </h1>
      <p className="font-poppins font-light text-white/60 max-w-md">
        Your payment could not be processed or was cancelled. No charges were
        made to your account.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 mt-10">
        <button
          onClick={() => navigate("/carts")}
          className="bg-white text-black py-3.5 px-8 font-poppins font-medium cursor-pointer hover:bg-neutral-200 transition-all duration-300"
        >
          Return to Cart
        </button>
        <button
          onClick={() => navigate("/")}
          className="border border-white py-3.5 px-8 text-white font-poppins font-medium cursor-pointer hover:bg-white hover:text-black transition-all duration-300"
        >
          Back to Home
        </button>
      </div>
    </div>
  );
};

export default FailedPayment;
