import React, { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );
  const [user, setUser] = useState(() =>
    localStorage.getItem("authTokens")
      ? jwt_decode(localStorage.getItem("authTokens"))
      : null
  );
  const [loading, setLoading] = useState(true);
  const [loginLoading, setLoginLoading] = useState(null);
  const baseURL = "https://cs404-project.herokuapp.com/service";

  const navigate = useNavigate();

  const loginUser = async (displayName, password) => {
    setLoginLoading(true);
    const response = await fetch(baseURL + "/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        displayName,
        password,
      }),
    });
    await response.json().then(function (data) {
      if (response.status === 200) {
        setAuthTokens(data);
        setUser(jwt_decode(data.access));
        localStorage.setItem("authTokens", JSON.stringify(data));
        localStorage.setItem("loggedInUser", JSON.stringify(data.user));
        setLoginLoading(false);
      } else {
        alert("ERROR: " + data);
        setLoginLoading(null);
      }
    });
  };

  const registerUser = async (displayName, password, github) => {
    const response = await fetch(baseURL + "/auth/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        displayName,
        password,
        github,
      }),
    });

    if (response.status === 201) {
      navigate("/login");
    } else {
      response.json().then(function (value) {
        alert("ERROR: " + value);
      });
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    localStorage.removeItem("user_id");
    navigate("/login");
  };

  const contextData = {
    user,
    setUser,
    authTokens,
    setAuthTokens,
    registerUser,
    loginUser,
    logoutUser,
    baseURL,
  };

  useEffect(() => {
    if (authTokens) {
      setUser(jwt_decode(authTokens.access));
      localStorage.setItem("user_id", user.user_id.split("/").pop());
    }
    setLoading(false);
  }, [authTokens, loading]);

  // Waits user to be set before sending user to main page. Otherwise user would be null
  // and the homepage will show nothing because it would fetch to /service/authors/null/posts/.
  // This is due to async between setting the user in loginUser & the above useEffect hook
  useEffect(() => {
    if (loginLoading !== null && loginLoading === false) {
      navigate("/stream");
    }
    setLoginLoading(null);
  }, [loginLoading]);

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  );
};
