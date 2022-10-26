import React, { useContext, useState } from "react";
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

function RenderAuthors(props) {
  // given the list of authors from the query, creates the user cards
  console.log(props.authors)
  if (props.authors) {
    return (
      <div className="authors-explore-container">
        {
        typeof props.authors !== 'undefined' ? props.authors.map((author) => <UserCard author={author}/>) : null
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

  const search = async val => {
    setLoading(true);
    const res = await search2(
      `${baseURL}/authors?search=${val}`      // TODO: need to search with pagination
    );
    console.log(res);
    setAuthors(res);

    setLoading(false);
  };

  const onChangeHandler = async e => {
    search(e.target.value);
    setValue(e.target.value);
  }

  const api = useAxios();
  const { baseURL } = useContext(AuthContext);

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
    </div>
  );
}
