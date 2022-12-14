import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import axios from "axios"

// const baseURL = "https://cs404-project.herokuapp.com/service";

const useAxios = () => {
  // Use this function when you want to use a method that requires 
  // authorization. See FollowButton.jsx for an example use.
  const { authTokens, setUser, setAuthTokens, baseURL, logoutUser } = useContext(AuthContext);

  const axiosInstance = axios.create({
    baseURL,
    headers: { Authorization: `Bearer ${authTokens.access}` }
  });

  axiosInstance.interceptors.request.use(async req => {
    // intercepts the outgoing request and checks if the 
    // token is still valid (i.e. not expired)
    // if expired, refreshes it before letting the request continue
    const user = jwt_decode(authTokens.access);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

    if (!isExpired) return req;

    const response = await axios.post(`${baseURL}/auth/refresh/`, {
      refresh: authTokens.refresh
    });

    if (response.status === 401) {
      logoutUser();
    }

    localStorage.setItem("authTokens", JSON.stringify(response.data));

    setAuthTokens(response.data);
    setUser(jwt_decode(response.data.access));

    req.headers.Authorization = `Bearer ${response.data.access}`;
    return req;
  });

  return axiosInstance;
};

export default useAxios;