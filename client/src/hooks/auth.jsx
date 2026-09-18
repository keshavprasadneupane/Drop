import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(
    () => localStorage.getItem("dropp_access_token") || null,
  );
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem("dropp_user");
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);

  // Sync token to localStorage and validate session
  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem("dropp_access_token");
      if (savedToken) {
        try {
          const res = await api.get("/users/me/");
          if (res.data && res.data.user) {
            setUser(res.data.user);
            localStorage.setItem("dropp_user", JSON.stringify(res.data.user));
          }
        } catch {
          // Token expired or invalid
          setToken(null);
          setUser(null);
          localStorage.removeItem("dropp_access_token");
          localStorage.removeItem("dropp_user");
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = useCallback(async (email, password) => {
    const res = await api.post("/users/login/", { email, password });
    const accessToken = res.data.access_token;
    const userData = res.data.user;

    setToken(accessToken);
    setUser(userData);
    localStorage.setItem("dropp_access_token", accessToken);
    if (userData) {
      localStorage.setItem("dropp_user", JSON.stringify(userData));
    }
    return res.data;
  }, []);

  const signup = useCallback(async (name, email, username, password) => {
    const res = await api.post("/users/post/", {
      fullName: name,
      email,
      username,
      password,
    });
    const accessToken = res.data.access_token || res.data.tokens?.accessToken;
    const userData = res.data.user || res.data.data;

    if (accessToken) {
      setToken(accessToken);
      localStorage.setItem("dropp_access_token", accessToken);
    }
    if (userData) {
      setUser(userData);
      localStorage.setItem("dropp_user", JSON.stringify(userData));
    }
    return res.data;
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("dropp_access_token");
    localStorage.removeItem("dropp_user");
  }, []);

  const isAuthenticated = Boolean(token && user);

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated,
        loading,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export default useAuth;
