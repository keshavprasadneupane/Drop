import React from "react";
import { useNavigate } from "react-router-dom";
import MenArrivals from "../../assets/images/menArrivals.jpg";
import WomenArrivals from "../../assets/images/womenArrivals.jpg";
import { Description } from "../../components/componentsLayout";

const Arrivals = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col sm:flex-row items-center justify-center w-full">
      <button
        onClick={() => navigate("/men-collection")}
        className="relative group overflow-hidden cursor-pointer duration-300 w-full sm:w-1/2 h-64 sm:h-140 md:h-96 lg:h-240"
      >
        <img
          src={MenArrivals}
          alt="Men's New Arrival"
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 transition-opacity duration-300 group-hover:opacity-100 px-4 text-center">
          <Description descriptionTexts="Men's New Arrival" />
        </div>
      </button>
      <button
        onClick={() => navigate("/women-collection")}
        className="relative group overflow-hidden cursor-pointer duration-300 w-full sm:w-1/2 h-64 sm:h-140 md:h-96 lg:h-240"
      >
        <img
          src={WomenArrivals}
          alt="Women's New Arrival"
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 transition-opacity duration-300 group-hover:opacity-100 px-4 text-center">
          <Description descriptionTexts="Women's New Arrival" />
        </div>
      </button>
    </div>
  );
};

export default Arrivals;
