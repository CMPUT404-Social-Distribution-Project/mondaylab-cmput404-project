import React, { useContext, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Dropdown, InputGroup, Form, Button } from 'react-bootstrap';
import { BiDotsVerticalRounded } from "react-icons/bi";
import { MdModeEdit, MdDelete } from "react-icons/md";
import Card from 'react-bootstrap/Card';
import AuthContext from '../../context/AuthContext';
import "./PostCard.css";
import useAxios from "../../utils/useAxios";
import { confirmAlert } from 'react-confirm-alert';
import { useEffect } from 'react';
import EditPost from "./EditPost";


export default function PostCard(props) {
  const user_id = localStorage.getItem("user_id");
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const { authTokens } = useContext(AuthContext);
  const [postComment, setPostComment] = useState({
    comment: "",
  });
  const [comments, setComments] = useState([]);
  const [showEditPost, setShowEditPost] = useState(false);
  const api = useAxios();

  useEffect(() => {
      api
        .get(`${baseURL}/authors/${user_id}/posts/${props.post.uuid}/comments`)
        .then((response) => {
          if(response.data.items === undefined) {
            setComments(["No comments"]);
          } else {
            setComments(response.data.items);
          }
        })
        .catch((error) => {
          console.log(error);
        });
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
  }

  const confirmDelete = (uuid) => {
    confirmAlert({
      title: 'Confirm to submit',
      message: 'Are you sure to do this.',
      buttons: [
        {
          label: 'Yes',
          onClick: () => {deletePost(uuid)}
        },
        {
          label: 'No',
        }
      ]
    });
  };

  const sendComment = (uuid) => {
    api
      .post(`${baseURL}/authors/${user_id}/posts/${uuid}/comments/`, postComment)
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
            {<Dropdown.Item onClick={() => setShowEditPost(true)}><MdModeEdit /> Edit Post</Dropdown.Item>}
            {<Dropdown.Item className="delete-post" onClick={() => deletePost(props.post.uuid)}><MdDelete /> Delete Post</Dropdown.Item>}
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
        {showEditPost && <EditPost show={showEditPost} onHide={() => setShowEditPost(false)} post={props.post} />}

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
            <div className="comments">
              {comments.map((comment) => (
                  comment
              ))}
            </div>
          </div>
          <div className="input-comment">
            <InputGroup className="mb-3">
              <Form.Control
                placeholder="Comment"
                aria-label="Comment"
                onChange={(e) => (setPostComment({...postComment, comment: e.target.value}))
                }
              />
              <Button style={
                  {borderRadius: '15px', color: 'black', backgroundColor: '#BFEFE9'}
                }
                onClick={() => sendComment(props.post.uuid)}
              >
                Send
              </Button>
            </InputGroup>
          </div>
        </div>

      </Card.Body>
    </Card>
  );
}
