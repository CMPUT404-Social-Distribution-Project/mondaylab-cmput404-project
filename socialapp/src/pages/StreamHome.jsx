import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import "./pages.css";
import "./Profile.css";
import AuthContext from "../context/AuthContext";
import { Container } from "react-bootstrap";
import PostCard from "../components/Posts/PostCard";
import { BsGithub } from "react-icons/bs";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Popup from "reactjs-popup";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

export default function StreamHome() {
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const [postsArray, setPostsArray] = useState([]);
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const [liked, setLiked] = useState();
  const user_id = localStorage.getItem("user_id");
  const api = useAxios();
  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/stream/github`);
  };
  /**
   * Once the homepage starts rendering, we make an api call and get all posts owner by the current user and insert them into an array
   * however any issues or errors a logged to the console.
   *
   */

  const base = baseURL + /authors/ + user_id + /posts/;
  const [nextUrl, setNextUrl] = useState();
  const [previousUrl, setPreviousURL] = useState();
  useEffect(() => {
    const fetchData = async () => {
      await api
        .get(`${baseURL}/authors/${user_id}/posts/`)
        .then((response) => {
          setNextUrl(response.data.next);
          setPreviousURL(response.data.previous);
          setPostsArray(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
    };
    fetchData();
  }, [useLocation().state]);

  const paginationHandler = (url) => {
    try{
      axios.get(url)
      .then((response) => {
        setNextUrl(response.data.next);
        setPreviousURL(response.data.previous);
        setPostsArray(response.data.items);
      });
    }
    catch (error) {
      console.log(error);
    }
  }
  
  useEffect(() => {
    const fetchData = async () => {
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
  }, []);

  return (
    /**
     * We return a container that has the header and all of the posts, which are created by mapping each individual post to the PostCard js file
     * which has the format for each post object.
     *
     */

    <div className="homepage">
      <Row>
        <Col md={4}>
          <h1>My Feed</h1>
        </Col>
        <Col md={{ span: 4, offset: 4 }}>
          <Popup
            trigger={
              <button style={{ background: "none", border: "none" }}>
                <BsGithub
                  style={{
                    color: "var(--white-teal)",
                    marginTop: "1em",
                    marginBottom: "1em",
                    marginRight: "1em",
                  }}
                  onClick={routeChange}
                />
              </button>
            }
            on="hover"
            contentStyle={{ backgroundColor: "var(--dark-blue)", border: "none", width: "fit-content", padding: "0.5rem" }}
            arrowStyle={{ color: "var(--dark-blue)", stroke: "none"}}
            arrow={true}
          >
            <span style={{ fontSize: "0.8rem" }}> Click to see GitHub activities! </span>
          </Popup>
        </Col>
      </Row>
      <Container style={{ zIndex: 10 }}>
        <div className="posts">
          {postsArray.map((post) => (
            <PostCard loggedInAuthorsLiked={liked} loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} key={post.id} />
          ))}
        </div>
      </Container>

      <nav className="page">
        <ul className="pagination justify-content-center">
          {previousUrl &&
            <li className="page-item">
            <button className="page-link" onClick={()=>paginationHandler(previousUrl)}>{'<'}</button>
            </li>
          }
          {nextUrl &&
            <li className="page-item">
              <button className="page-link" onClick={()=>paginationHandler(nextUrl)}>{'>'}</button>
            </li> 
          }   
        </ul> 
      </nav>
    </div>
  );
}
