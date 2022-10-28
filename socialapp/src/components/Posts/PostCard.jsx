import React, { useState, useEffect, useContext } from 'react';
import ReactMarkdown from 'react-markdown';
import { Dropdown } from 'react-bootstrap';
import { BiDotsVerticalRounded } from "react-icons/bi";
import Card from 'react-bootstrap/Card';
import AuthContext from '../../context/AuthContext';
import "./PostCard.css";
import useAxios from "../../utils/useAxios";



export default function PostCard(props) {
  const user_id = localStorage.getItem("user_id");
  const [isOwner, setIsOwner] = useState(true);
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const { authTokens } = useContext(AuthContext);
  const api = useAxios();
  
  useEffect (() => {

  }, []);

  const deletePost = (uuid) => {
      api
        .delete(`${baseURL}/authors/${user_id}/posts/${uuid}`)
        .then((response) => {
          console.log(response.data);
          window.location.reload(true);
        })
        .catch((error) => {
          alert(`Something went wrong posting! \n Error: ${error}`)
          console.log(error);
        });
  };

  // only render options if the user viewing it is the author of it
  function PostOptions () {
    if (user_id === props.post.author.uuid) {
      return (
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
      );
    } else {
      return (<></>);
    }
  }

  return (
    <Card className="post-card"style={{ width: '30rem', whiteSpace: "nowrap"}}>
      <Card.Header>
        <div className="post-author">
          <div className="profile-pic-post">
            <img src={props.post.author.profileImage} alt="profilePic"/>
          </div>
          <div className="post-author-name">{props.post.author.displayName}</div>
        </div>
        <PostOptions />
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
