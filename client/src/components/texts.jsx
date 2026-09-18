export const HeroHeading = ({ headingName }) => {
  return (
    <h1 className="flex text-white font-poppins font-medium text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl text-center leading-tight">
      {headingName}
    </h1>
  );
};

export const Description = ({ descriptionTexts }) => {
  return (
    <h1 className="flex text-white/80 font-poppins font-medium text-sm sm:text-base md:text-lg text-center">
      {descriptionTexts}
    </h1>
  );
};

export const DescriptionBlack = ({ descriptionTexts }) => {
  return (
    <h1 className="flex text-black/80 font-poppins font-medium text-sm sm:text-base md:text-lg text-center">
      {descriptionTexts}
    </h1>
  );
};

export const Heading = ({ headingName }) => {
  return (
    <h1 className="flex text-black font-poppins font-medium text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-[80px] text-center leading-tight">
      {headingName}
    </h1>
  );
};

export const SubHeading = ({ headingName }) => {
  return (
    <h1 className="flex text-black font-poppins font-light text-xl sm:text-2xl md:text-3xl lg:text-[40px] text-center">
      {headingName}
    </h1>
  );
};

export const PricingText = ({price}) => {
  return (
    <h1 className="font-poppins font-medium text-sm sm:text-base">
      {price}
    </h1>
  )
}

export const NavsTexts = ({pageName}) => {
  return (
    <h1 className="font-poppins text-black font-medium text-sm sm:text-base lg:text-xl">
      {pageName}
    </h1>
  )
}