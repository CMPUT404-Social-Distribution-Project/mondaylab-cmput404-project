import React, { useContext, useState, useEffect } from "react";
import "./pages.css";
// import * as Yup from "yup";
import useAxios from "../utils/useAxios.js";
import AuthContext from "../context/AuthContext";
import UserCard from "../components/UserCard";
import { search2 } from "../utils/searchUtil";
import "./Explore.css";
import { FaSearch } from "react-icons/fa";
import ExplorePostCard from "../components/Posts/ExplorePostCard";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import { useLocation } from "react-router-dom";

function RenderAuthors(props) {
  // given the list of authors from the query, creates the user cards
  if (props.authors) {
    return (
      <div className="authors-explore-container">
        {typeof props.authors.items !== "undefined" ? (
          props.authors.items.length !== 0 ? (
            props.authors.items.map((author) => <UserCard author={author} key={author.id}/>)
          ) : (
            <Card style={{ backgroundColor: "var(--darker-blue)" }}>
              <h5 style={{ marginLeft: "15px" }}>
                No match result for authors!
              </h5>
            </Card>
          )
        ) : null}
      </div>
    );
  }
  return <></>;
}

function RenderRemoteAuthors(props) {
  // given the list of authors from the query, creates the user cards
  if (props.authors !== "undefined" && props.authors.length > 0) {
    return (
        <Card className="remote-authors-container" style={{ backgroundColor: "var(--darker-blue)" }}>
          <Card.Body>
            <h5>Remote Authors</h5>
          {props.authors.map((author) => <UserCard author={author} key={author.id}/>)}
          </Card.Body>
        </Card>
    );
  }
}

export default function Explore() {
  // const validate = Yup.object().shape({
  //   search: Yup.string(),
  // });
  const [authors, setAuthors] = useState(null);
  const [loading, setLoading] = useState(false);
  const [value, setValue] = useState("");
  const [postsArray, setPostsArray] = useState([]);
  const [searchPostsArray, setSearchPostsArray] = useState([]);
  const [displaySearch, setDisplaySearch] = useState(false);
  const api = useAxios();
  const { baseURL } = useContext(AuthContext);
  const [remoteAuthors, setRemoteAuthors] = useState([]);
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const user_id = localStorage.getItem("user_id"); // the currently logged in author

  useEffect(() => {
    const fetchData = async () => {
      api
      .get(`${baseURL}/posts/`)
      .then((response) => {
        setPostsArray(response.data.items);
      })
      .catch((error) => {
        console.log(error);
      });
      api
        .get(`${baseURL}/node/authors/`)
        .then((response) => {
          setRemoteAuthors(response.data.items);
        })
        .catch((error) => {
          console.log(error);
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
    }
    fetchData();
  }, [useLocation().state]);

  useEffect(() => {

  }, []);

  const search = async (val) => {
    setLoading(true);
    const res = await search2(
      `${baseURL}/authors?search=${val}` // TODO: need to search with pagination
    );
    setAuthors(res);

    setLoading(false);
  };

  const searchPosts = (val) => {
    setLoading(true);
    var searchPosts = [];
    setSearchPostsArray([]);
    for (let i = 0; i < postsArray.length; i++) {
      if (postsArray[i].title.indexOf(val) > -1) {
        searchPosts.push(postsArray[i]);
        setSearchPostsArray((searchPostsArray) => [
          ...searchPostsArray,
          postsArray[i],
        ]);
      }
    }
    if (searchPosts.length === 0) {
      setDisplaySearch(false);
    } else {
      setDisplaySearch(true);
    }
    setLoading(false);
  };

  const onChangeHandler = async (e) => {
    search(e.target.value);
    setValue(e.target.value);
    searchPosts(e.target.value);
  };

  return (
    <div className="explore-page-container">
      {/* Stack the columns on mobile by making one full-width and the other half-width */}
      <Row className="explore-title-container">
        <Col>
          <h1>Explore</h1>
        </Col>
        <Col className="search-col">
          <FaSearch className="FaSearch" />
          <input
            className="search-bar-explore"
            value={value}
            onChange={(e) => onChangeHandler(e)}
            placeholder="Search for an author/post"
          />
        </Col>
        <Col className="empty-rec" />
      </Row>
      <div className="searchResult">
        {value !== "" ? <RenderAuthors authors={authors} /> : null}
      </div>

      {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
      <div className="public-posts-and-remote-container">
        <Card style={{ backgroundColor: "var(--darker-blue)" }}>
          <Card.Body>
            {value !== "" ? (
              displaySearch === true ? (
                <>
                  <p>Search posts:</p>
                  <Row>
                    {searchPostsArray.map((post) => (
                      <Col key={post.id} >
                        <ExplorePostCard loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} />
                      </Col>
                    ))}
                  </Row>
                </>
              ) : (
                <h5> No match result for posts!</h5>
              )
            ) : (
              <>
                <h5>Current public posts</h5>
                <div className="all-posts-container">
                  {postsArray.map((post) => (
                      <ExplorePostCard loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} key={post.id} />
                  ))}
                </div>
              </>
            )}
          </Card.Body>
        </Card>
        <RenderRemoteAuthors authors={remoteAuthors}/>

      </div>
      

    </div>
  );
}
