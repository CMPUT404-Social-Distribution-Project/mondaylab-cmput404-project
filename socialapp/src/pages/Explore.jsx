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
import PostCard from "../components/Posts/PostCard";
function RenderAuthors(props) {
  // given the list of authors from the query, creates the user cards
  console.log(props.authors)
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
    console.log(res);
    setAuthors(res);

    setLoading(false);
  };
  const searchPosts = val => {
    setLoading(true);
    var searchPosts=[]
    setSearchPostsArray([]);
    for (let i = 0; i < postsArray.length; i++) {
      console.log("==", postsArray[i].title, "--", val)
      if (postsArray[i].title.indexOf( val ) > -1 ){       
        searchPosts.push(postsArray[i])
        setSearchPostsArray(searchPostsArray => [...searchPostsArray, postsArray[i]]); 
      }
    }
    if (searchPosts.length==0){
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
    <div className="explore-container">
      <h1>Explore</h1>
      <div className="search-bar-container">
        <FaSearch className="FaSearch"/>
        <input
            className="search-bar-explore"
            value={value}
            onChange={e => onChangeHandler(e)}
            placeholder="Search for an author"
            />
      </div>
      {<RenderAuthors authors={authors}/>}



      {
      value!="" ? 
      displaySearch == true ?
      
      searchPostsArray.map((post) => (
      <><p> search result</p>
      <PostCard
          post={post}
          key={post.id} /></>
      )): <h1> No match result for posts</h1>
      : postsArray.map((post) => (
        <PostCard
          post={post}
          key={post.id} />
      ))
        }


    </div>
  );
}
