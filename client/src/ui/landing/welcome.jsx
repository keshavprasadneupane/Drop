import React from "react";
import { useNavigate } from "react-router-dom";
import { Heading, SubHeading } from "../../components/componentsLayout";

const Welcome = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col py-20 px-4 sm:px-6">
      <div className="flex flex-col gap-extrasmall items-center justify-center text-center">
        <Heading headingName="Welcome to the world of DROPP :)" />
        <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-mid">
          <button
            onClick={() => navigate("/about")}
            className="underline font-poppins font-light text-xl sm:text-2xl md:text-3xl lg:text-[40px] cursor-pointer hover:text-blue-500 duration-300 bg-transparent border-none"
          >
            Read our Story
          </button>
          <SubHeading headingName="and" />
          <button
            onClick={() => navigate("/about")}
            className="underline font-poppins font-light text-xl sm:text-2xl md:text-3xl lg:text-[40px] cursor-pointer hover:text-blue-500 duration-300 bg-transparent border-none"
          >
            Meet the Makers
          </button>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
