import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import Logo from "../assets/images/logo.png";
import { useToast } from "../hooks/toast";
import useAuth from "../hooks/auth";

const Signup = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [passwordError, setPasswordError] = useState("");
  const [serverError, setServerError] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const { showToast } = useToast();
  const { signup } = useAuth();

  const searchParams = new URLSearchParams(location.search);
  const redirectUrl = searchParams.get("redirect") || "/";

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (passwordError) setPasswordError("");
    if (serverError) setServerError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setPasswordError("Passwords do not match");
      showToast("Passwords do not match", "error");
      return;
    }

    setIsLoading(true);
    setServerError("");

    try {
      await signup(
        formData.name,
        formData.email,
        formData.username,
        formData.password,
      );

      showToast(
        `Account created! Welcome to DROPP, ${formData.name}!`,
        "success",
      );

      navigate(redirectUrl);
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Unable to create account. Please try again.";
      setServerError(message);
      showToast(message, "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen w-full font-poppins">
      <div
        className="hidden lg:block lg:w-1/2 bg-cover bg-center"
        style={{
          backgroundImage:
            "url('https://i.pinimg.com/736x/12/e2/9b/12e29bf350f6d1604d32925ae31ffbf0.jpg')",
        }}
      />
      <div className="flex flex-1 flex-col items-center justify-center bg-black px-6 sm:px-12 py-16">
        <div className="w-full max-w-sm flex flex-col gap-8">
          <Link to="/" className="self-center">
            <img
              src={Logo}
              alt="DROPP Logo"
              className="h-7 hover:scale-105 transition-transform"
            />
          </Link>

          <div className="flex flex-col gap-2 text-center">
            <h1 className="font-poppins font-medium text-2xl sm:text-3xl text-white">
              Create your account
            </h1>
            <p className="font-poppins font-light text-sm text-white/60">
              Sign up to track orders, save favourites, and check out faster.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="name"
                className="font-poppins text-xs text-white/60"
              >
                Full name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleChange}
                className="bg-transparent border-b border-white/30 py-2 text-sm font-poppins text-white placeholder:text-white/30 focus:outline-none focus:border-white transition-colors duration-300"
                placeholder="Nischal Pokharel"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="email"
                className="font-poppins text-xs text-white/60"
              >
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="bg-transparent border-b border-white/30 py-2 text-sm font-poppins text-white placeholder:text-white/30 focus:outline-none focus:border-white transition-colors duration-300"
                placeholder="neeschal@example.com"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="username"
                className="font-poppins text-xs text-white/60"
              >
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="bg-transparent border-b border-white/30 py-2 text-sm font-poppins text-white placeholder:text-white/30 focus:outline-none focus:border-white transition-colors duration-300"
                placeholder="Enter your desired username"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="password"
                className="font-poppins text-xs text-white/60"
              >
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                minLength={6}
                value={formData.password}
                onChange={handleChange}
                className="bg-transparent border-b border-white/30 py-2 text-sm font-poppins text-white placeholder:text-white/30 focus:outline-none focus:border-white transition-colors duration-300"
                placeholder="At least 6 characters"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="confirmpassword"
                className="font-poppins text-xs text-white/60"
              >
                Confirm Password
              </label>
              <input
                id="confirmpassword"
                name="confirmPassword"
                type="password"
                required
                minLength={6}
                value={formData.confirmPassword}
                onChange={handleChange}
                className="bg-transparent border-b border-white/30 py-2 text-sm font-poppins text-white placeholder:text-white/30 focus:outline-none focus:border-white transition-colors duration-300"
                placeholder="Confirm your password"
              />
              {passwordError && (
                <span className="text-xs text-red-400 font-poppins mt-1">
                  {passwordError}
                </span>
              )}
              {serverError && (
                <span className="text-xs text-red-400 font-poppins mt-1">
                  {serverError}
                </span>
              )}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="mt-2 bg-white text-black font-poppins font-medium text-sm py-3 cursor-pointer transition-all duration-300 ease-out hover:bg-white/85 hover:-translate-y-0.5 disabled:opacity-50"
            >
              {isLoading ? "Creating account..." : "Create account"}
            </button>
          </form>

          <p className="font-poppins font-light text-sm text-white/60 text-center">
            Already have an account?{" "}
            <Link
              to={
                redirectUrl !== "/"
                  ? `/login?redirect=${encodeURIComponent(redirectUrl)}`
                  : "/login"
              }
              className="text-white underline underline-offset-2"
            >
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
