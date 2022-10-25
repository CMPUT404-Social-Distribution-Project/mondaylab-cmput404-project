import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import "./Profile.css";
import default_profile_pic from "../des/default_profile_pic.jpg";
import FollowButton from "../components/FollowButton";
import { useParams } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";
import EditProfileButton from "../components/EditProfileButton";

export default function Profile() {
  const [author, setAuthor] = useState("");               // the response object we get (Author object)  
  const [postsArray, setPostsArray] = useState(""); 
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");  // the currently logged in author
  const { id } = useParams();                       // gets the author id in the url
  const api = useAxios();

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      await axios
        .get(`${baseURL}/authors/${id}/`)
        .then((response) => {
          setAuthor(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
      await api      
        .get(`${baseURL}/authors/${id}/posts/`)
        .then((response) => {
          setPostsArray(response.data);
          console.log("Got posts of author")
          console.log(response.data);
        })
        .catch((error) => {
          console.log("Failed to get posts of author. " + error);
        });
    };
    fetchData();
  }, []);

  return (
    <div className="profileContainer">
      <div className="profileHeader">
        <div className="profilePicWithFollowButton">
          <div className="profilePicPage">
            <img id="profilePicPage" src={author.profileImage} alt="profilePic"/>
          </div>
          <FollowButton id={id}/>
        </div>

        <div className="profileInfo">
          <div className="profileName">{author.displayName}</div>
          <div className="profileStats">
            <div id="statContainer" className="followers">
              <span>Followers:</span>
              {/* Issue with data not becoming fully available due to async operations;
              So just do 0 until we get the full info */}
              <div className="infoNum">{typeof author.followers === 'undefined' ? 0 : author.followers.length}</div>
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
          <EditProfileButton className="edit-button" author={author}/>
        </div>
      </div>

      <div className="posts">
        {
          typeof postsArray.items !== 'undefined' ? 
            postsArray.items.map((post) => <PostCard post={post} />)
            : null
     
          
        }
      </div>
    </div>
  );
}
