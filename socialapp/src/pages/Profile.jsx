import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import "./Profile.css";
import default_profile_pic from "../des/default_profile_pic.jpg";
import { useParams } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";
import UserCard from "../components/UserCard";
import EditProfileButton from "../components/Profile/EditProfileButton";
import FollowButton from "../components/Profile/FollowButton";
import ProfileTabs from "../components/Profile/ProfileTabs";

function ProfilePosts(props) {
  return (
    <div className="posts">
    {
      typeof props.postsArray.items !== 'undefined' ? 
        props.postsArray.items.map((post) => <PostCard post={post} />)
        : null
    }
    </div>
  )
}

function ProfileFollowers(props) {
  return (
    <div className="followers">
    {
      typeof props.postsArray !== 'undefined' ? 
        props.postsArray.map((follower) => <UserCard author={follower}/>)
        : null
    }
    </div>
  );
}


export default function Profile() {
  const [author, setAuthor] = useState("");               // the response object we get (Author object)  
  const [postsArray, setPostsArray] = useState(""); 
  const [followersArray, setFollowersArray] = useState(""); 
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");  // the currently logged in author
  const { author_id, dir } = useParams();                       // gets the author id in the url
  const api = useAxios();
  console.log(dir);

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      await axios
        .get(`${baseURL}/authors/${author_id}/`)
        .then((response) => {
          setAuthor(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
      await api      
        .get(`${baseURL}/authors/${author_id}/posts/`)
        .then((response) => {
          setPostsArray(response.data);
          console.log("Got posts of author")
          console.log(response.data);
        })
        .catch((error) => {
          console.log("Failed to get posts of author. " + error);
        });
      await api      
        .get(`${baseURL}/authors/${author_id}/followers/`)
        .then((response) => {
          setFollowersArray(response.data.items);
          console.log("Got followers of author")
          console.log(response.data.items);
        })
        .catch((error) => {
          console.log("Failed to get followers of author. " + error);
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
          <FollowButton id={author_id}/>
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
      <ProfileTabs dir={dir} author_id={author_id}/>
      {dir === 'posts' || dir === undefined ? <ProfilePosts postsArray={postsArray}/> : <></>}
      {dir === 'followers' ? <ProfileFollowers followersArray={followersArray}/> : <></>}

    </div>
  );
}
