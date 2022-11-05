import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import { useParams, useLocation } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";


export default function Post() {
  const [post, setPost] = useState(""); 
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");  // the currently logged in author
  const { author_id, post_id } = useParams();                       // gets the author id in the url
  const api = useAxios();

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      await api      
        .get(`${baseURL}/authors/${author_id}/posts/${post_id}`)
        .then((response) => {
          setPost(response.data);
          console.log("Got post of author")
          console.log(response.data);
        })
        .catch((error) => {
          console.log("Failed to get post of author. " + error);
        });
    };
    fetchData();
  }, [useLocation().state]);

  return (
    <div className="post-container">
        {post && <PostCard post={post} />}

    </div>
  );
}
