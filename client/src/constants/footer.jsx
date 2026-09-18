import React, { useState } from "react";

const footerLinks = [
  {
    title: "Shop",
    links: [
      { name: "Women", href: "/women-collection" },
      { name: "Men", href: "/men-collection" },
      { name: "New Arrivals", href: "/sales" },
      { name: "Sale", href: "/sales" },
    ],
  },
  {
    title: "Company",
    links: [
      { name: "Our Story", href: "#" },
      { name: "Meet the Makers", href: "#" },
      { name: "Careers", href: "#" },
      { name: "Sustainability", href: "#" },
    ],
  },
  {
    title: "Support",
    links: [
      { name: "Contact Us", href: "#" },
      { name: "FAQs", href: "#" },
      { name: "Shipping & Returns", href: "#" },
      { name: "Size Guide", href: "#" },
    ],
  },
];

const socialLinks = [
  { name: "Instagram", href: "#" },
  { name: "TikTok", href: "#" },
  { name: "X", href: "#" },
  { name: "Pinterest", href: "#" },
];

const Footer = () => {
  const [email, setEmail] = useState("");

  const handleSubscribe = (e) => {
    e.preventDefault();
    setEmail("");
  };

  return (
    <footer className="w-full bg-black text-white px-4 sm:px-6 lg:px-mid pt-12 sm:pt-16 lg:pt-20 pb-8">
      <div className="flex flex-col lg:flex-row lg:justify-between gap-10 lg:gap-large pb-12 sm:pb-16 border-b border-white/20">
        <div className="flex flex-col gap-3 sm:gap-mid max-w-md">
          <h2 className="font-poppins font-medium text-xl sm:text-2xl lg:text-3xl">
            Join the DROPP list
          </h2>
          <p className="font-poppins font-light text-sm sm:text-base text-white/70">
            Be first to know about new arrivals, exclusive drops, and offers.
          </p>
          <form
            onSubmit={handleSubscribe}
            className="flex flex-col sm:flex-row gap-3 mt-2 w-full"
          >
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="flex-1 bg-transparent border border-white/40 px-4 py-3 text-sm font-poppins text-white placeholder:text-white/50 focus:outline-none focus:border-white transition-colors duration-300"
            />
            <button
              type="submit"
              className="shrink-0 bg-white text-black font-poppins font-medium text-sm px-6 py-3 cursor-pointer transition-all duration-300 ease-out hover:bg-white/80 hover:-translate-y-0.5"
            >
              Subscribe
            </button>
          </form>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-6 gap-y-8 sm:gap-x-10 lg:gap-x-extralarge">
          {footerLinks.map((column) => (
            <div key={column.title} className="flex flex-col gap-3 sm:gap-mid">
              <h3 className="font-poppins font-medium text-sm sm:text-base">
                {column.title}
              </h3>
              <ul className="flex flex-col gap-2 sm:gap-3">
                {column.links.map((link) => (
                  <li key={link.name}>
                    <a
                      href={link.href}
                      className="font-poppins font-light text-sm text-white/70 hover:text-white transition-colors duration-300"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
      <div className="flex flex-col-reverse sm:flex-row items-center justify-between gap-6 sm:gap-4 pt-6 sm:pt-8">
        <p className="font-poppins font-light text-xs sm:text-sm text-white/50 text-center sm:text-left">
          © {new Date().getFullYear()} DROPP. All rights reserved.
        </p>
        <div className="flex items-center gap-4 sm:gap-6">
          {socialLinks.map((social) => (
            <a
              key={social.name}
              href={social.href}
              className="font-poppins font-light text-xs sm:text-sm text-white/70 hover:text-white transition-colors duration-300"
            >
              {social.name}
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
};

export default Footer;