import React, { useContext, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Dropdown, InputGroup, Form, Button, Container } from 'react-bootstrap';
import { BiDotsVerticalRounded } from "react-icons/bi";
import { MdModeEdit, MdDelete } from "react-icons/md";
import Card from 'react-bootstrap/Card';
import AuthContext from '../../context/AuthContext';
import "./PostCard.css";
import useAxios from "../../utils/useAxios";
import { confirmAlert } from 'react-confirm-alert';
import { useEffect } from 'react';
import EditPost from "./EditPost";
import CommentCard from './CommentCard';
import { BsFillChatFill, BsFillHeartFill } from "react-icons/bs";


export default function PostCard(props) {
  const user_id = localStorage.getItem("user_id");
  const post_user_id = props.post.author.uuid;
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const { authTokens } = useContext(AuthContext);
  const [postComment, setPostComment] = useState({
    comment: "",
  });
  const [comments, setComments] = useState([]);
  const [showEditPost, setShowEditPost] = useState(false);
  const api = useAxios();
  const [likeCount, setLikeCount] = useState(0);
  const [CommentCount, setCommentCount] = useState(0);
  const [color, setColor] = useState("white");
  const [author, setAuthor] = useState(""); 
  const [open, openComments] = useState(false)
  /* // display liked if a post is already liked
  if (like == null) {
    props.liked.forEach((element) => {
      if (element.object == props.post.url) {
        setLike(true);
      }
    });
    if (like !== null) {
      setLike(false);
    }
  }
    // like a post
    const likeHandler = () => {
      setLike(true);
      dispatch(likePost(props.post.url, post_author_id));
      setNumLikes(props.post.numLikes);
    }; */
  // Called after rendering. Fetches data
  const sendLike=(uuid) => {
    const postLike ={"type": "like", 
                    "summary":`${author.displayName} Likes your post.`, 
                    "author": author,
                    "object": props.post.id};
    console.log(postLike)
    api      
    .post(`${baseURL}/authors/${post_user_id}/inbox/`, postLike)
    .then((response) => {
  
      setColor("red")
      setLikeCount(likeCount=> likeCount+1)
    })
    .catch((error) => {
      console.log("Failed to get posts of author. " + error);
    });


  };

  useEffect(() => {
        const fetchData = async () => {
          await api
            .get(`${baseURL}/authors/${user_id}/`)
            .then((response) => {
              setAuthor(response.data);
            })
            .catch((error) => {
              console.log(error);
            });
            await api
          .get(`${baseURL}/authors/${post_user_id}/posts/${props.post.uuid}/likes`)
          .then((response) => {
              console.log("2222", response.data.items) ;
              setLikeCount(likeCount=>response.data.items.length);
              
            })
          .catch((error) => {
            console.log(error);
          });
          await api
          .get(`${baseURL}/authors/${post_user_id}/posts/${props.post.uuid}/comments/`)
          .then((response) => {
              const commentArray = response.data.comments;
              setCommentCount(commentArray.length);
              if(commentArray.length !== 0) {
                for (let i = 0; i < commentArray.length; i++){
                  const comment = commentArray[i];
                  setComments(comments => [...comments, comment]);
                }
              }
            })
          .catch((error) => {
            console.log(error);
          });
          };
          fetchData();
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
    <Card className="post-card">
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
        <div> 
          <BsFillHeartFill 
          style={{color:likeCount!=0? "red": "white"}}
          onClick={() => sendLike(props.post.uuid)}
          />
          
       {likeCount==0? 0: likeCount}
       <BsFillChatFill 
       style={{color:CommentCount!=0? "yellow": "white" , marginLeft:'30px'}}
       onClick={() => openComments(!open)}
       />
       {
        open?
          <div className="comments-text">
                        Comments
                      <div className="comments" style={{marginTop: "5%"}}>
                        <Container>
                          {(() => {
                            if(comments.length === 0){
                              return (
                              <p>No Comments</p>
                              )
                          } else {
                              return (
                                <div>
                                  {comments.map((comment) => (
                                    <CommentCard 
                                      author = {comment.author}
                                      comment={comment.comment} 
                                    />
                                  ))}
                                </div>
                              )
                          }})()}
                        </Container>
                      </div>
                    </div>
        : 
        null
       }
       {comments.length}
        </div>
        <div className="comments-container">
         
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
