import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import "./pages.css";
import AuthContext from "../context/AuthContext";
import "./Profile.css";
import { useParams } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";
import { Container } from "react-bootstrap";

export default function StreamHome() {
  const [posts, setPosts] = useState([])
  const user_id = localStorage.getItem("user_id");  // the currently logged in author

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/service/authors/${user_id}/posts/`, { params: { visibility: "Public" } })
      .then((response) => {
        setPosts(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  })

  return (
    <div>
      <h1>Posts</h1>
      <Container>
        {posts.map((posts) => (
          <div>
              <PostCard props="posts"/>
          </div>
        ))}
      </Container>
    </div>
  );
}
