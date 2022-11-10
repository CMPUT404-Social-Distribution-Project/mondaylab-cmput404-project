import React, { useContext, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Dropdown, InputGroup, Form, Button, Container } from "react-bootstrap";
import { BiDotsVerticalRounded } from "react-icons/bi";
import { MdModeEdit, MdDelete, MdShare } from "react-icons/md";
import { IoUnlink } from "react-icons/io5";
import { FaUserFriends } from "react-icons/fa";
import Card from "react-bootstrap/Card";
import AuthContext from "../../context/AuthContext";
import "./PostCard.css";
import useAxios from "../../utils/useAxios";
import { confirmAlert } from "react-confirm-alert";
import { useEffect } from "react";
import EditPost from "./EditPost";
import CommentCard from "./CommentCard";
import { BsFillChatFill, BsFillHeartFill } from "react-icons/bs";
import { useNavigate, useLocation } from "react-router-dom";

export default function PostCard(props) {
  const user_id = localStorage.getItem("user_id");
  const post_user_id = props.post.author.uuid;
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
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
  const [open, openComments] = useState(false);
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);

  // if the post is an image post, don't show it's content,
  // since it contains a base64 string. Which is very long.
  const [showContent, setShowContent] = useState(() => {
    if (props.post.contentType.startsWith("image")) {
      return false;
    } else {
      return true;
    }
  });

  // for navigating to post's author
  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${post_user_id}/`, { state: { refresh: true } });
  };

  // for refreshing the page of where the post card is
  const location = useLocation();
  const refreshState = () => {
    navigate(`${location.pathname}`, { state: { refresh: true } });
  };

  const sendPostLike = (uuid) => {
    const postLike = {
      type: "like",
      summary: `${author.displayName} Likes your post.`,
      author: author,
      object: props.post.id,
    };
    api
      .post(`${baseURL}/authors/${post_user_id}/inbox/`, postLike)
      .then((response) => {
        setColor("var(--orange)");
        setLikeCount((likeCount) => likeCount + 1);
      })
      .catch((error) => {
        console.log(error);
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
        .get(
          `${baseURL}/authors/${post_user_id}/posts/${props.post.uuid}/likes`
        )
        .then((response) => {
          setLikeCount((likeCount) => response.data.items.length);
        })
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(
          `${baseURL}/authors/${post_user_id}/posts/${props.post.uuid}/comments/`
        )
        .then((response) => {
          const commentArray = response.data.comments;
          setCommentCount(commentArray.length);
          if (commentArray.length !== 0) {
            for (let i = 0; i < commentArray.length; i++) {
              const comment = commentArray[i];
              setComments((comments) => [...comments, comment]);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(
          `${baseURL}/authors/${user_id}/followers`
        )
        .then((response) => {
          setFollowers(response.data.items)})
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(
          `${baseURL}/authors/${user_id}/friends/`
        )
        .then((response) => {
          setFriends(response.data.items)})
        .catch((error) => {
          console.log(error);
        });
    }
    fetchData();
  }, []);

  const sharePost = (post) => {
    console.log(post.id)
    if (post.visibility === "PUBLIC") {
      for(let index = 0; index < followers.length; index++) {
        const sharedPost = {
          type: "post",
          summary: `${author.displayName} shared a post.`,
          author: author,
          object: post.id,
        };
        api
          .post(`${baseURL}/authors/${followers[index].uuid}/inbox/`, post)
          .then((response) => {
            console.log(response)
          })
          .catch((error) => {
            console.log("Failed to get posts of author. " + error);
          });
      }
    } else if (post.visibility === "FRIENDS") {
      for(let index = 0; index < friends.length; index++) {
        const sharedPost = {
          type: "post",
          summary: `${author.displayName} shared a post.`,
          author: author,
          object: post.id,
        };
        api
          .post(`${baseURL}/authors/${friends[index].uuid}/inbox/`, post)
          .then((response) => {
            console.log(response)
          })
          .catch((error) => {
            console.log("Failed to get posts of author. " + error);
          });
      }
    }
  };

  const deletePost = (uuid) => {
    api
      .delete(`${baseURL}/authors/${user_id}/posts/${uuid}`)
      .then((response) => {
        window.location.reload(true);
      })
      .catch((error) => {
        alert(`Something went wrong posting! \n Error: ${error}`);
        console.log(error);
      });
  };

  const confirmDelete = (uuid) => {
    confirmAlert({
      title: "Confirm to submit",
      message: "Are you sure youn want to delete this post?",
      buttons: [
        {
          label: "Yes",
          onClick: () => {
            deletePost(uuid);
          },
        },
        {
          label: "No",
        },
      ],
    });
  };

  const sendComment = (uuid) => {
    var commentObject = {};
    api
      .post(
        `${baseURL}/authors/${user_id}/posts/${uuid}/comments/`,
        postComment
      )
      .then((response) => {
        window.location.reload(true);

        commentObject["type"] = response.data.type;
        commentObject["comment"] = response.data.comment;
        commentObject["author"] = response.data.author;
        commentObject["id"] = response.data.id;
        commentObject["contentType"] = response.data.contentType;
        commentObject["published"] = response.data.published;
        commentObject["uuid"] = response.data.uui;

        api
          .post(`${baseURL}/authors/${post_user_id}/inbox/`, commentObject)
          .then((response) => {
            console.log("success send comments to inbox");
          })
          .catch((error) => {
            console.log("Failed to get posts of author. " + error);
          });
      })
      .catch((error) => {
        alert(`Something went wrong posting! \n Error: ${error}`);
        console.log(error);
      });
  };

  // only render options if the user viewing it is the author of it
  function PostOptions() {
    return (
      <div className="options">
        <Dropdown>
          <Dropdown.Toggle id="dropdown-basic">
            <BiDotsVerticalRounded />
          </Dropdown.Toggle>
          <Dropdown.Menu>
            <Dropdown.Item onClick={() => sharePost(props.post)}>
              <MdShare /> Share Post
            </Dropdown.Item>
            {(() => {
              if (user_id === props.post.author.uuid) {
                return (
                  <div>
                    <Dropdown.Item onClick={() => setShowEditPost(true)}>
                      <MdModeEdit /> Edit Post
                    </Dropdown.Item>

                    <Dropdown.Item
                      className="delete-post"
                      onClick={() => confirmDelete(props.post.uuid)}
                    >
                      <MdDelete /> Delete Post
                    </Dropdown.Item>
                  </div>
                )
              }
            })()}
          </Dropdown.Menu>
        </Dropdown>
      </div>
    );
  }

  return (
    <Card className="post-card">
      <Card.Header>
        <div className="post-author" onClick={routeChange}>
          <div className="profile-pic-post">
            <img src={props.post.author.profileImage} alt="profilePic" />
          </div>
          <div className="post-author-name">
            {props.post.author.displayName}
          </div>
        </div>
        {props.post.visibility === "FRIENDS" ? (
          <div className="friends-indicator">
            <FaUserFriends />
            Friends-Only
          </div>
        ) : (
          <div className="friends-indicator" style={{ background: "none" }} />
        )}
        {props.post.unlisted === true ? (
          <div className="unlisted-indicator" style={{
            margin: props.post.visibility === "FRIENDS" ? "0 1rem 0 0" : "0 1rem 0 auto"
          }}>
            <IoUnlink />
            Unlisted
          </div>
        ) : (
          <div className="unlisted-indicator" style={{ 
            background: "none",
            margin: "0",
            padding: "0" 
            }} 
          />
        )}
        <PostOptions />
        {showEditPost && (
          <EditPost
            show={showEditPost}
            onHide={() => {
              setShowEditPost(false);
              refreshState(navigate, location);
            }}
            post={props.post}
          />
        )}
      </Card.Header>
      <Card.Body>
        <Card.Title>
          <ReactMarkdown>{props.post.title}</ReactMarkdown>
        </Card.Title>
        {props.post.image && (
          <img className="post-image" src={props.post.image} alt="postImage" />
        )}
        <Card.Text>
          {showContent && <ReactMarkdown>{props.post.content}</ReactMarkdown>}
        </Card.Text>
        <hr />
        <div className="like-comment-container">
          <BsFillHeartFill
            className="like-icon"
            style={{
              color: likeCount !== 0 ? "var(--orange)" : "var(--white-teal)",
            }}
            onClick={() => sendPostLike(props.post.uuid)}
          />

          {likeCount === 0 ? 0 : likeCount}

          <BsFillChatFill
            className="comment-icon"
            style={{
              color: CommentCount !== 0 ? "var(--teal)" : "var(--white-teal)",
              marginLeft: "30px",
            }}
            onClick={() => openComments(!open)}
          />
          {comments.length}

          <MdShare className="share-icon" onClick={() => sharePost(props.post)}/>
        </div>
        <div>
          {open ? (
            <div className="comments-text">
              Comments
              <div className="comments" style={{ marginTop: "1rem" }}>
                <Container>
                  {(() => {
                    if (comments.length === 0) {
                      return <p>No Comments</p>;
                    } else {
                      return (
                        <div>
                          {comments.map((comment, i) => (
                            <CommentCard
                              key={i}
                              author={comment.author}
                              comment={comment.comment}
                            />
                          ))}
                        </div>
                      );
                    }
                  })()}
                </Container>
              </div>
            </div>
          ) : null}
        </div>
        <div className="comments-container">
          <div className="input-comment">
            <InputGroup className="mb-3">
              <Form.Control
                placeholder="Comment"
                aria-label="Comment"
                onChange={(e) =>
                  setPostComment({ ...postComment, comment: e.target.value })
                }
              />
              <Button
                style={{
                  borderRadius: "1.5rem",
                  color: "black",
                  backgroundColor: "#BFEFE9",
                }}
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
