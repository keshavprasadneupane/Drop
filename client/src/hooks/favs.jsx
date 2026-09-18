import { createContext, useContext, useState, useEffect, useCallback } from "react";

const FavouritesContext = createContext(null);

const getInitialFavs = () => {
  try {
    const stored = localStorage.getItem("dropp_favs");
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

export const FavouritesProvider = ({ children }) => {
  const [favList, setFavList] = useState(getInitialFavs);

  useEffect(() => {
    localStorage.setItem("dropp_favs", JSON.stringify(favList));
  }, [favList]);

  const addToFavourites = useCallback((product) => {
    setFavList((prev) => {
      const exists = prev.some(
        (item) => item.item === product.item && item.itemName === product.itemName
      );
      if (exists) return prev;
      return [...prev, product];
    });
  }, []);

  const removeFromFavourites = useCallback((index) => {
    setFavList((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const toggleFavourite = useCallback((product) => {
    setFavList((prev) => {
      const existingIndex = prev.findIndex(
        (item) => item.item === product.item && item.itemName === product.itemName
      );
      if (existingIndex > -1) {
        return prev.filter((_, i) => i !== existingIndex);
      }
      return [...prev, product];
    });
  }, []);

  const isFavourite = useCallback(
    (product) => {
      return favList.some(
        (item) => item.item === product.item && item.itemName === product.itemName
      );
    },
    [favList]
  );

  return (
    <FavouritesContext.Provider
      value={{
        favList,
        setFavList,
        addToFavourites,
        removeFromFavourites,
        toggleFavourite,
        isFavourite,
      }}
    >
      {children}
    </FavouritesContext.Provider>
  );
};

const useFavs = () => {
  const context = useContext(FavouritesContext);
  if (!context) {
    throw new Error("useFavs must be used within a FavouritesProvider");
  }
  return context;
};

export default useFavs;
