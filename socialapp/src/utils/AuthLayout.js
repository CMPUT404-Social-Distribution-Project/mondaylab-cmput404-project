import { Navigate, Outlet } from 'react-router-dom';
import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import axios from "axios";

const AuthLayout = () => {
    let { user, authTokens, setUser, setAuthTokens, baseURL, logoutUser } = useContext(AuthContext);
    if (authTokens === null) {
      logoutUser();
      return <Navigate to={"/login"} replace />
    }
    const userToken = jwt_decode(authTokens.access);
    let isExpired = dayjs.unix(userToken.exp).diff(dayjs()) < 1;
    
    // if token is expired, try to refresh it
    if (isExpired === true) {
        const req = async () => {
            await axios.post(`${baseURL}/auth/refresh/`, {
                refresh: authTokens.refresh
              })
              .then((response) => {
                // set the new access token
                localStorage.setItem("authTokens", JSON.stringify(response.data));
                setAuthTokens(response.data);
                // set our user object again
                setUser(jwt_decode(response.data.access));
                // isExpired no longer true, set it to false, so user stays logged in
                isExpired = false;
              })
              .catch((err) => {
                console.log("Failed to refresh token.");
              });
        }
        req();
    }

    if (user !== null ) {
        // if the token has expired or doesn't exist, log the user out, otherwise
        // show them the protected pages
        if (isExpired === true || isExpired === null) {
          logoutUser();
          return <Navigate to={"/login"} replace />;
          
        } else {
          return <Outlet />
        }
    }
    return <Navigate to={"/login"} replace />;
};

export default AuthLayout;