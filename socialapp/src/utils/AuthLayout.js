import { Navigate, Outlet } from 'react-router-dom';
import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";

const AuthLayout = () => {
    let { user } = useContext(AuthContext);
    if (user !== null) {
        const isAuthenticated = user;
        return isAuthenticated ? <Outlet /> : null; // or loading indicator, etc...
    }
    return <Navigate to={"/login"} replace />;
};

export default AuthLayout;