import api from "./api";

const handleSignup = async (name, email, username, password) => {
  const data = {
    fullName: name,
    email: email,
    username: username,
    password: password,
  };

  try {
    const response = await api.post("/users/post/", data);
    return response.data;
  } catch (err) {
    console.error("Signup error:", err);
    throw err;
  }
};

export default handleSignup;
