import api from "./api";

export const handleLogin = async (email, password) => {
  const data = {
    email: email,
    password: password,
  };

  try {
    const response = await api.post("/users/login/", data);
    return response.data;
  } catch (err) {
    console.error("Login service error:", err);
    throw err;
  }
};

export default handleLogin;
