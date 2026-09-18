import React, { useEffect, useState } from "react";
import Navbar from "../../constants/navbar";
import {
  HeroHeading,
  Description,
  PrimaryButton,
} from "../../components/componentsLayout";

const Hero = () => {
  const backgroundImages = [
    "https://images.pexels.com/photos/29244128/pexels-photo-29244128.jpeg",
    "https://images.pexels.com/photos/5319503/pexels-photo-5319503.jpeg",
    "https://images.pexels.com/photos/34121563/pexels-photo-34121563.jpeg",
    "https://images.pexels.com/photos/17347429/pexels-photo-17347429.jpeg",
    "https://images.pexels.com/photos/9476356/pexels-photo-9476356.jpeg",
  ];

  const [currentImage, setCurrentImage] = useState(0);

  useEffect(() => {
    const handleInterval = setInterval(() => {
      setCurrentImage((previous) => (previous + 1) % backgroundImages.length);
    }, 5000);
    return () => clearInterval(handleInterval);
  }, [backgroundImages.length]);

  return (
    <section className="relative w-full h-screen overflow-hidden">
      {backgroundImages.map((image, index) => (
        <div
          key={image}
          aria-hidden="true"
          className={`absolute inset-0 flex flex-col gap-y-6 sm:gap-y-8 lg:gap-large items-center justify-center bg-cover bg-center px-4 sm:px-6 text-center transition-opacity duration-1000 ease-in-out ${
            index === currentImage ? "opacity-100" : "opacity-0"
          }`}
          style={{ backgroundImage: `url('${image}')` }}
        >
          <div className="flex flex-col items-center justify-center gap-y-2 sm:gap-y-3">
            <HeroHeading headingName="Stay the night" />
            <Description descriptionTexts="JUST DROPPED: FALL / WINTER 2026" />
          </div>
          <div className="flex flex-col sm:flex-row w-full sm:w-auto gap-3 sm:gap-mid px-6 sm:px-0">
            <PrimaryButton navigateTo="/women-collection" buttonName="Shop Women's" />
            <PrimaryButton navigateTo="/men-collection" buttonName="Shop Men's" />
          </div>
        </div>
      ))}
      <div className="absolute top-0 left-0 w-full z-20">
        <Navbar />
      </div>
    </section>
  );
};
export default Hero;