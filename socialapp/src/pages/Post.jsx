import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import { useParams, useLocation } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";
import { useNavigate } from "react-router-dom";


export default function Post() {
  const [post, setPost] = useState(""); 
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");  // the currently logged in author
  const { author_id, post_id } = useParams();                       // gets the author id in the url
  const api = useAxios();
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const [liked, setLiked] = useState([]);
  

  // route to 404 if post not found
  const navigate = useNavigate();
  const routeChange = () => {
      navigate(`/404`, {state: {refresh:true}});
  }

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      await api      
        .get(`${baseURL}/authors/${author_id}/posts/${post_id}`)
        .then((response) => {
          setPost(response.data);
          console.log(response.data);
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            console.log(error.response.status);
            routeChange();
          }
        });
      await api
        .get(`${baseURL}/authors/${user_id}/followers`)
        .then((response) => {
          setFollowers(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(`${baseURL}/authors/${user_id}/friends/`)
        .then((response) => {
          setFriends(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(
          `${baseURL}/authors/${user_id}/liked`
        )
        .then((response) => {
          setLiked(response.data.items);
        })
        .catch((error) => {
          console.log(error);
      });
    };
    fetchData();
  }, [useLocation().state]);

  return (
    <div className="post-container">
        {post && <PostCard loggedInAuthorsLiked={liked} loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} />}

    </div>
  );
}
