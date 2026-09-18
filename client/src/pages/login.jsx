import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import Logo from "../assets/images/logo.png";
import { useToast } from "../hooks/toast";
import useAuth from "../hooks/auth";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const { showToast } = useToast();
  const { login } = useAuth();

  // Check if redirect query param exists
  const searchParams = new URLSearchParams(location.search);
  const redirectUrl = searchParams.get("redirect") || "/";

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (errorMsg) setErrorMsg("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg("");

    try {
      const data = await login(formData.email, formData.password);
      const name = data.user?.fullName || formData.email.split("@")[0];
      showToast(`Welcome back, ${name}!`, "success");
      navigate(redirectUrl);
    } catch (err) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Login failed. Please check your credentials.";
      setErrorMsg(message);
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
              Log In
            </h1>
            <p className="font-poppins font-light text-sm text-white/60">
              {redirectUrl !== "/"
                ? "Please log in to continue with your checkout"
                : "Login with your existing account in order to continue!"}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
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
                value={formData.password}
                onChange={handleChange}
                className="bg-transparent border-b border-white/30 py-2 text-sm font-poppins text-white placeholder:text-white/30 focus:outline-none focus:border-white transition-colors duration-300"
                placeholder="Enter your password"
              />
            </div>

            {errorMsg && (
              <p className="text-xs text-red-400 font-poppins leading-relaxed">
                {errorMsg}
              </p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="mt-2 bg-white text-black font-poppins font-medium text-sm py-3 cursor-pointer transition-all duration-300 ease-out hover:bg-white/85 hover:-translate-y-0.5 disabled:opacity-50"
            >
              {isLoading ? "Logging in..." : "Login"}
            </button>
          </form>

          <p className="font-poppins font-light text-sm text-white/60 text-center">
            New to Dropp?{" "}
            <Link
              to={
                redirectUrl !== "/"
                  ? `/signup?redirect=${encodeURIComponent(redirectUrl)}`
                  : "/signup"
              }
              className="text-white underline underline-offset-2"
            >
              Signup
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
