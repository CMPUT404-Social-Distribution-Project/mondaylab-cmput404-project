import React, { useState, useEffect, useContext } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
import { Dropdown } from 'react-bootstrap';
import { BiDotsVerticalRounded } from "react-icons/bi";
import Card from 'react-bootstrap/Card';
import AuthContext from '../../context/AuthContext';
import "./PostCard.css";
import { confirmAlert } from 'react-confirm-alert';

export default function PostCard(props) {
  const user_id = localStorage.getItem("user_id");
  const [isOwner, setIsOwner] = useState(true);
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const { authTokens } = useContext(AuthContext);
  
  useEffect (() => {

  }, []);

  const deletePost = (uuid) => {
      axios
        .delete(`${baseURL}/authors/${user_id}/posts/${uuid}`, { headers: { 'Authorization': `Bearer ${authTokens.access}` } })
        .then((response) => {
          console.log(response.data);
          window.location.reload(true);
        })
        .catch((error) => {
          alert(`Something went wrong posting! \n Error: ${error}`)
          console.log(error);
        });
  };

  return (
    <Card style={{ width: '30rem', whiteSpace: "nowrap"}}>
      <Card.Header style={{width: '200%'}}>
        <div style={{display: "inline-block"}} className="profilePicPage">
          <img id="profilePicPage" src={props.post.author.profileImage} alt="profilePic"/>
        </div>
        <div className="options">
          <Dropdown>
            <Dropdown.Toggle id="dropdown-basic">
              <BiDotsVerticalRounded />
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {isOwner && <Dropdown.Item onClick={() => deletePost(props.post.uuid)}>Delete Post</Dropdown.Item>}
            </Dropdown.Menu>  
          </Dropdown>
        </div>
      </Card.Header>
      <Card.Img variant="top" src="" />
      <Card.Body>
        <Card.Title>
          <ReactMarkdown>{props.post.title}</ReactMarkdown>
        </Card.Title>
        <Card.Text>
          <ReactMarkdown>{props.post.content}</ReactMarkdown>
        </Card.Text>
        <hr/>
        <div className="comments-container">
          <div className="comments-text">
              Comments
          </div>
          <div className="comments">
              {/* show max 5 comments, have option to show more */}
          </div>
        </div>

      </Card.Body>
    </Card>
  );
}
