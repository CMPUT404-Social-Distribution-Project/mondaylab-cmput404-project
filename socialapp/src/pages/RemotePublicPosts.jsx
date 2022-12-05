import { React, useState, useEffect, useContext } from 'react';
import './pages.css';
import ExplorePostCard from '../components/Posts/ExplorePostCard';
import PulseLoader from 'react-spinners/PulseLoader';
import AuthContext from '../context/AuthContext';
import useAxios from '../utils/useAxios';
import { toast } from 'react-toastify';
import { useLocation } from "react-router-dom";
import Card from "react-bootstrap/Card";

export default function RemotePublicPosts() {
  const [postsArray, setPostsArray] = useState([]);
  const [postsLoading, setPostsLoading] = useState(false);
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const [liked, setLiked] = useState([]);
  const { baseURL } = useContext(AuthContext);
  const api = useAxios();
  const user_id = localStorage.getItem("user_id"); // the currently logged in author

  useEffect(() => {
    const fetchData = async () => {
      setPostsLoading(true);
      api
      .get(`${baseURL}/node/posts/`)
      .then((response) => {
        setPostsArray(response.data.items);
        setPostsLoading(false);
      })
      .catch((error) => {
        setPostsLoading(false);
        toast.error("Failed to fetch remote public posts.");
        console.log("Failed to fetch remote public posts.", error);
      });
      await api
        .get(`${baseURL}/authors/${user_id}/followers/`)
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
    }
    fetchData();
  }, [useLocation().state]);

  return (
    <Card style={{ backgroundColor: "var(--darker-blue)" }}>
          <Card.Body className="public-posts-container">
            { 
              <>
                <h5>Current remote public posts</h5>
                {postsLoading ? <PulseLoader className="public-posts-loader" color="var(--teal)" /> : <div className="all-posts-container">
                  {postsArray.map((post) => (
                      <ExplorePostCard loggedInAuthorsLiked={liked} loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} key={post.id} />
                  ))}
                </div>}
                
              </>
            }
          </Card.Body>
    </Card>
  )
}
