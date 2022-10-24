import React, { useEffect, useState, useContext} from 'react';
import axios from 'axios';
import "./pages.css";
import "./Profile.css";
import AuthContext from "../context/AuthContext";
import { Container } from 'react-bootstrap';
import PostCard from "../components/Posts/PostCard";

export default function StreamHome() {
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const [postsArray, setPostsArray] = useState([]);
  const user_id = localStorage.getItem("user_id");

  useEffect(() => {
    axios
        .get(`${baseURL}/authors/${user_id}/posts/`)
        .then((response) => {
          setPostsArray(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
  }, []);

  return (
    <div className='homepage'>
      <Container style={{ zIndex: 10 }}>
          <h1>My Feed</h1>
          <div classNme = "posts">
            {postsArray.map((post) => (
              <PostCard post = {post}/>
            ))}
        </div>
        </Container>
    </div>
  );
}
