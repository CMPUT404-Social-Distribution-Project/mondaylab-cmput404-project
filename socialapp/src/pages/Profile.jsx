import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import "./Profile.css";
import default_profile_pic from "../des/default_profile_pic.jpg";


export default function Profile() {
  const [res, setRes] = useState("");
  const api = useAxios();
  const { user } = useContext(AuthContext);
  // const user_id = user.user_id.split("/").pop();
  const user_id = localStorage.getItem("user_id");


  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      axios
        .get(`http://127.0.0.1:8000/service/authors/${user_id}/`)
        .then((response) => {
          console.log(response.data);
          setRes(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    };
    fetchData();
  }, []);

  return (
    <div className="profileContainer">
      <div className="profileHeader">
        <div className="profilePicPage">
          <img id="profilePicPage" src={default_profile_pic} alt="profilePic"/>
        </div>
        <div className="profileInfo">
          <div className="profileName">{res.displayName}</div>
          <div className="profileStats">
            <div id="statContainer" className="followers">
              <text>Followers:</text>
              <div className="infoNum">100000000</div>
            </div>
            <div id="statContainer" className="following">
              <text>Following:</text>
              <div className="infoNum">100000000</div>
            </div>
            <div id="statContainer" className="friends">
              <text>Friends:</text>
              <div className="infoNum">100000000</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
