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
  const baseURL = "http://127.0.0.1:8000/service";

  const navigate = useNavigate();

  const loginUser = async (displayName, password) => {
    const response = await fetch(baseURL + "/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        displayName,
        password
      })
      
    });
    await response.json().then(function(data) {
      if (response.status === 200) {
        setAuthTokens(data);
        setUser(jwt_decode(data.access));
        localStorage.setItem("authTokens", JSON.stringify(data));
        navigate("/stream");
      } else {
        console.log(data)
        alert("ERROR: " + data);
      }
    });


  };
  
  const registerUser = async (displayName, password, github) => {
    const response = await fetch(baseURL + "/auth/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        displayName,
        password,
        github,

      }) 
    });

    if (response.status === 201) {
      navigate("/login");
    } else {
      response.json().then(function(value) {
        alert("ERROR: " + value);
      })
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    localStorage.removeItem("user_id");
    navigate("/");
  };

  const contextData = {
    user,
    setUser,
    authTokens,
    setAuthTokens,
    registerUser,
    loginUser,
    logoutUser,
    baseURL
  };

  useEffect(() => {
    if (authTokens) {
      setUser(jwt_decode(authTokens.access));
      localStorage.setItem("user_id", user.user_id.split("/").pop());
    }
    setLoading(false);
  }, [authTokens, loading]);

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  );
};