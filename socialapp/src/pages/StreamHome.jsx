import React, { useEffect, useState, useContext} from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import "./Profile.css";
import AuthContext from "../context/AuthContext";
import { Container } from 'react-bootstrap';
import PostCard from "../components/Posts/PostCard";

export default function StreamHome() {
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const [postsArray, setPostsArray] = useState([]);
  const user_id = localStorage.getItem("user_id");
  const api = useAxios();

  /**
   * Once the homepage starts rendering, we make an api call and get all posts owner by the current user and insert them into an array
   * however any issues or errors a logged to the console.
   * 
   */

  useEffect(() => {
    api
        .get(`${baseURL}/authors/${user_id}/posts/`)
        .then((response) => {
          setPostsArray(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
  }, []);

  return (
    /**
     * We return a container that has the header and all of the posts, which are created by mapping each individual post to the PostCard js file
     * which has the format for each post object. 
     * 
     */
    
    <div className='homepage'>
      <Container style={{ zIndex: 10 }}>
          <h1>My Feed</h1>
          <div classNme = "posts">
            {postsArray.map((post) => (
              <PostCard 
                post = {post}
                key = {post.id}
              />
            ))}
        </div>
        </Container>
    </div>
  );
}
