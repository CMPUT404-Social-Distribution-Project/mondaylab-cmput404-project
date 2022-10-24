import { Navigate, Outlet } from 'react-router-dom';
import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import axios from "axios";

const AuthLayout = () => {
    let { user, authTokens, setUser, setAuthTokens, baseURL } = useContext(AuthContext);
    const userToken = jwt_decode(authTokens.access);
    const isExpired = dayjs.unix(userToken.exp).diff(dayjs()) < 1;
    
    // if token is expired, try to refresh it
    if (isExpired === true) {
        const req = async () => {
            const response = await axios.post(`${baseURL}/refresh/`, {
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
    }


    if (user !== null ) {
        let isAuthenticated = user;
        // if the token has expired or doesn't exist, log the user out, otherwise
        // show them the protected pages
        if (isExpired === true || isExpired === null) {
            isAuthenticated = false;
        }
        return isAuthenticated ? <Outlet /> : <Navigate to={"/login"} replace />; // or loading indicator, etc...
    }
    return <Navigate to={"/login"} replace />;
};

export default AuthLayout;