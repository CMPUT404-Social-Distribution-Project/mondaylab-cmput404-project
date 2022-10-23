import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import "./Profile.css";
import default_profile_pic from "../des/default_profile_pic.jpg";
import FollowButton from "../components/FollowButton";
import { useParams } from "react-router-dom";

export default function Profile() {
  const [res, setRes] = useState("");
  const api = useAxios();
  const { baseURL } = useContext(AuthContext);
  const user_id = localStorage.getItem("user_id");
  const { id } = useParams();   // gets the author id in the url

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      await axios
        .get(`${baseURL}/authors/${id}/`)
        .then((response) => {
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
        <div className="profilePicWithFollowButton">
          <div className="profilePicPage">
            <img id="profilePicPage" src={res.profileImage} alt="profilePic"/>
          </div>
          <FollowButton id={id}/>
        </div>

        <div className="profileInfo">
          <div className="profileName">{res.displayName}</div>
          <div className="profileStats">
            <div id="statContainer" className="followers">
              <span>Followers:</span>
              {/* Issue with data not becoming fully available due to async operations;
              So just do 0 until we get the full info */}
              <div className="infoNum">{typeof res.followers === 'undefined' ? 0 : res.followers.length}</div>
            </div>
            <div id="statContainer" className="following">
              <span>Following:</span>
              <div className="infoNum">100000000</div>
            </div>
            <div id="statContainer" className="friends">
              <span>Friends:</span>
              <div className="infoNum">100000000</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
