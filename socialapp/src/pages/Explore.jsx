import React, { useContext, useState, useEffect, useRef } from "react";
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
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import PulseLoader from 'react-spinners/PulseLoader';
import { toast } from 'react-toastify';
import ReactPaginate from "react-paginate";
function TeamSelect(props) {
  return (
    <DropdownButton onSelect={props.onSelect} title={"Team " + props.title} >
      <Dropdown.Item eventKey="2">Team 2</Dropdown.Item>
      <Dropdown.Item eventKey="3">Team 3</Dropdown.Item>
      <Dropdown.Item eventKey="4">Team 4</Dropdown.Item>
      <Dropdown.Item eventKey="16">Team 16</Dropdown.Item>
    </DropdownButton>
  );
}

export default function Explore() {
  const [authors, setAuthors] = useState(null);
  const [loading, setLoading] = useState(false);
  const [value, setValue] = useState("");
  const [postsArray, setPostsArray] = useState([]);
  const [postsArrayP, setPostsArrayP] = useState([]);
  const [searchPostsArray, setSearchPostsArray] = useState([]);
  const [displaySearch, setDisplaySearch] = useState(false);
  const api = useAxios();
  const { baseURL } = useContext(AuthContext);
  const [remoteAuthors, setRemoteAuthors] = useState([]);
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const [liked, setLiked] = useState([]);
  const user_id = localStorage.getItem("user_id"); // the currently logged in author
  const storedTeamSelected = localStorage.getItem("teamSelected");
  const [teamSelected, setTeamSelected] = useState(() => storedTeamSelected ? storedTeamSelected : "2");
  const [postsLoading, setPostsLoading] = useState(false);
  const [remoteAuthorsLoading, setRemoteAuthorsLoading] = useState(false);
  const [showSearchedAuthors, setShowSearchedAuthors] = useState(false);
  const [pageCount, setPageCount]= useState(1);
  const [stopIncreasePageCount, setStopIncreasePageCount]=useState(false);
  
  /**
 * Hook that alerts clicks outside of the passed ref
 * Ref: https://stackoverflow.com/questions/32553158/detect-click-outside-react-component
 * Answer by: Ben Bud
 */
function useOutsideAlerter(ref) {
  useEffect(() => {
    /**
     * Alert if clicked on outside of element
     */
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        setShowSearchedAuthors(false);
      }
    }
    // Bind the event listener
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      // Unbind the event listener on clean up
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref]);
}


function RenderAuthors(props) {
  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef);
  // given the list of authors from the query, creates the user cards
  if (showSearchedAuthors && props.authors) {
    return (
      <div ref={wrapperRef} className="authors-explore-container">
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

  useEffect(() => {
    const fetchData = async () => {
      setPostsLoading(true);
      api
      .get(`${baseURL}/posts/?page=1&size=10`)
      .then((response) => {
        setPostsArrayP(response.data.items);
        console.log("---1",`${baseURL}/posts/?page=1&size=5` )
        console.log("---2", response.data.items.length, response)
        if (response.data.items.length!=0){setPageCount(pageCount+1)}
        console.log("===1", pageCount)
        setPostsLoading(false);
      })
      .catch((error) => {
        setPostsLoading(false);
        toast.error("Failed to fetch all public posts.");
        console.log("Failed to fetch all public posts.", error);
      });
      setRemoteAuthorsLoading(true);
      api
        .get(`${baseURL}/node/authors/?team=${teamSelected}`)
        .then((response) => {
          setRemoteAuthors(response.data.items);
          setRemoteAuthorsLoading(false);
        })
        .catch((error) => {
          setRemoteAuthorsLoading(false);
          toast.error("Failed to fetch selected team's remote authors.");
          console.log("Failed to fetch selected team's remote authors.", error);
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

  useEffect(() => {

  }, []);


  /*setPostsLoading(true);
      api
      .get(`${baseURL}/posts/`)
      .then((response) => {
        setPostsArray(response.data.items);
        setPostsLoading(false);
      })
      .catch((error) => {
        setPostsLoading(false);
        toast.error("Failed to fetch all public posts.");
        console.log("Failed to fetch all public posts.", error);
      });*/ 
  const [pagenum, setPageNum]=useState(0)

  const search = async (val) => {
    setLoading(true);
    const res = await search2(
      `${baseURL}/authors?size=10&search=${val}` // TODO: need to search with pagination
    );
    setAuthors(res);
    setShowSearchedAuthors(true);

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

  const fetchTeamAuthors = (e) => {
    setRemoteAuthorsLoading(true);
    api
      .get(`${baseURL}/node/authors/?team=${e}`)
      .then((response) => {
        setRemoteAuthors(response.data.items);
        setRemoteAuthorsLoading(false);
      })
      .catch((error) => {
        setRemoteAuthorsLoading(false);
        console.log(error);
      });
  }

  const handleTeamSelect = (e) => {
    setTeamSelected(e);
    fetchTeamAuthors(e);
    localStorage.setItem("teamSelected", e);
  }

  const loadPost = (event) => {
    setPostsLoading(true);
    api
    .get(`${baseURL}/posts/?page=${event.selected+1}&size=10`)
    .then((response) => {
      setPostsArrayP(response.data.items);
      if (response.data.items.length!=0 && stopIncreasePageCount===false){setPageCount(pageCount+1)}else{setStopIncreasePageCount(true)}
      console.log("---11",`${baseURL}/posts/?page=${event.selected+1}&size=10` )
      console.log("---22",pageCount, "---",  response)
      setPostsLoading(false);
    })
    .catch((error) => {
      setPostsLoading(false);
      toast.error("Failed to fetch all public posts.");
      console.log("Failed to fetch all public posts.", error);
    });
        setLoading(false);
    console.log(
      `User requested page number ${event.selected+1}`
    );

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

            {value !== "" ? <RenderAuthors authors={authors} /> : null}
  
        </Col>
        <Col className="empty-rec" />
      </Row>
      <div className="searchResult">
      </div>

      {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
      <div className="public-posts-and-remote-container">
        <Card style={{ backgroundColor: "var(--darker-blue)" }}>
          <Card.Body className="public-posts-container">
            {value !== "" ? (
              displaySearch === true ? (
                <>
                  <p>Search posts:</p>
                  <Row>
                    {searchPostsArray.map((post) => (
                      <Col key={post.id} >
                        <ExplorePostCard loggedInAuthorsLiked={liked} loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} />
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
                {postsLoading ? <PulseLoader className="public-posts-loader" color="var(--teal)" /> : <div className="all-posts-container">
                  {postsArrayP.map((post) => (
                      <ExplorePostCard loggedInAuthorsLiked={liked} loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={post} key={post.id} />
                  ))}
                </div>}
                
              </>
            )}
          </Card.Body>
        </Card>
        <Card className="remote-authors-container" style={{ backgroundColor: "var(--darker-blue)" }}>
          <Card.Body className="remote-authors-content">
            <h5>Remote Authors</h5>
            <TeamSelect
              onSelect={handleTeamSelect}
              title={teamSelected}
            />
            {remoteAuthorsLoading ? <PulseLoader className="remote-authors-loader" color="var(--teal)" /> : 
            remoteAuthors.map((author) => <UserCard author={author} key={author.id}/>)}

          </Card.Body>
        </Card>
        {/* <RenderRemoteAuthors authors={remoteAuthors}/> */}

      </div>
      <div style={{ marginLeft: "40%" }}>
            <ReactPaginate
              breakLabel="..."
              nextLabel="next >"
              onPageChange={loadPost}
              pageRangeDisplayed={5}
              pageCount={pageCount}
              marginPagesDisplayed={2}
              previousLabel="< previous"
              pageClassName="page-item"
              pageLinkClassName="page-link"
              previousClassName="page-item"
              previousLinkClassName="page-link"
              nextClassName="page-item"
              nextLinkClassName="page-link"
              breakClassName="page-item"
              breakLinkClassName="page-link"
              containerClassName="pagination"
              activeClassName="active"
            />
          </div>
      

    </div>
  );
}
