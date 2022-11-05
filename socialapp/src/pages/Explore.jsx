import React, { useContext, useState, useEffect } from "react";
import "./pages.css";
import TextField from "../components/TextField";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import useAxios from "../utils/useAxios.js";
import AuthContext from "../context/AuthContext";
import UserCard from "../components/UserCard"
import { search2 } from "../utils/searchUtil";
import "./Explore.css";
import { FaSearch } from "react-icons/fa";
import ExplorePostCard from "../components/Posts/ExplorePostCard";
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
function RenderAuthors(props) {
  // given the list of authors from the query, creates the user cards
  if (props.authors) {
    return (
      <div className="authors-explore-container">
        {
        typeof props.authors.items !== 'undefined' ? props.authors.items.map((author) => <UserCard author={author}/>) : null
        }
      </div>
    )
  }
  return <></>;
}

export default function Explore() {
  const validate = Yup.object().shape({
    search: Yup.string(),
  });
  const [authors, setAuthors] = useState(null); 
  const [loading, setLoading] = useState(false); 
  const [value, setValue] = useState(""); 
  const [postsArray, setPostsArray] = useState([]);
  const [searchPostsArray, setSearchPostsArray] = useState([]);
  const [displaySearch, setDisplaySearch] = useState(false); 
  const api = useAxios();
  const { baseURL } = useContext(AuthContext);

  useEffect(() => {
    api
        .get(`${baseURL}/posts/`)
        .then((response) => {
          setPostsArray(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
  }, []);

  const search = async val => {
    setLoading(true);
    const res = await search2(
      `${baseURL}/authors?search=${val}`      // TODO: need to search with pagination
    );
    setAuthors(res);

    setLoading(false);
  };

  const searchPosts = val => {
    setLoading(true);
    var searchPosts=[]
    setSearchPostsArray([]);
    for (let i = 0; i < postsArray.length; i++) {
      if (postsArray[i].title.indexOf( val ) > -1 ){       
        searchPosts.push(postsArray[i])
        setSearchPostsArray(searchPostsArray => [...searchPostsArray, postsArray[i]]); 
      }
    }
    if (searchPosts.length===0){
      setDisplaySearch(false)
    }else{
      setDisplaySearch(true)        
    }
    setLoading(false);
  };

  const onChangeHandler = async e => {
    search(e.target.value);
    setValue(e.target.value);
    searchPosts(e.target.value)
  }

  return (

    <Container>
    {/* Stack the columns on mobile by making one full-width and the other half-width */}
    <Row>
      <Col> <h1>Explore</h1> </Col>
      <Col>
        <input
              className="search-bar-explore"
              value={value}
              onChange={e => onChangeHandler(e)}
              placeholder="Search for an author/post"
              /> 
      </Col>
      <Col>
      <FaSearch className="FaSearch"/> 
      </Col>
      
      
    </Row>
    <div className="searchResult">{value!="" ? <RenderAuthors authors={authors}/>: null} </div>
    
    {/* Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop */}
    <Row>
      
      <Col>
      <Card style={{ width: '100%' , backgroundColor: 'var(--darker-blue)'}}>
      <Card.Body>
          {
                value!="" ? 
                displaySearch == true ?
                <><p>Search posts:</p>
                <Row>
                  {searchPostsArray.map((post) => (
                    <Col>
                          <ExplorePostCard 
                            post={post}
                            key={post.id} />


                    </Col>
                  ))}
                </Row></>: <h1> No match result for posts</h1>
                : 
                <><p>Current public posts</p>
                <Row >
                      {postsArray.map((post) => (
                        <Col>
                              <ExplorePostCard
                                post={post}
                                key={post.id} />

                        </Col>
                      ))}
                    </Row></>
              }
      </Card.Body>
    </Card>

    

      </Col>

   
      <Col  xs lg="2">
      <Card border="success" style={{ width: '18rem', height:'100%', backgroundColor: 'var(--darker-blue)'}}>
        <Card.Header>Friends</Card.Header>
        <Card.Body>
          <Card.Title>Search author</Card.Title>
          <Card.Text>
            we can discuss what we need to do here.
            maybe we can search author here, the left top one is search posts only
          </Card.Text>
        </Card.Body>
      </Card>
      </Col>
    </Row>

  </Container>
    

  );
}
