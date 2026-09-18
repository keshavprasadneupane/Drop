import React from "react";
import Navbar from "../constants/navbar";
import Footer from "../constants/footer";
import FavItems from "../ui/favourites/favitems";

const Favourites = () => {
  return (
    <div className="flex flex-col min-h-screen w-full bg-white font-poppins justify-between">
      <Navbar bgstate={true} />
      <main className="flex-1 w-full pt-20 sm:pt-24">
        <FavItems />
      </main>
      <Footer />
    </div>
  );
};

export default Favourites;
