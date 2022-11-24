import React, { useContext, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Dropdown, InputGroup, Form, Button, Container } from "react-bootstrap";
import { BiDotsVerticalRounded } from "react-icons/bi";
import { MdModeEdit, MdDelete, MdShare } from "react-icons/md";
import { IoUnlink } from "react-icons/io5";
import { FaUserFriends, FaLock } from "react-icons/fa";
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
import { extractAuthorUUID, extractPostUUID, authorHostIsOurs, createNodeObject, isValidHTTPUrl, emptyNode } from "../../utils/utils";

export default function PostCard(props) {
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const post_user_uuid = extractAuthorUUID(props.post.author.id);
  const post_id = extractPostUUID(props.post.id)
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service

  // node
  const [postAuthorNode, setPostAuthorNode] = useState(null);     // the node object of post's author
  const [postAuthorBaseApiURL, setPostAuthorBaseAPI] = useState("");

  const [postComment, setPostComment] = useState({
    comment: "",
    type: "comment",
    contentType: "text/markdown",
    author: loggedInUser
  });
  const [comments, setComments] = useState([]);
  const [showEditPost, setShowEditPost] = useState(false);
  const api = useAxios();
  const [likeCount, setLikeCount] = useState(null);
  const [CommentCount, setCommentCount] = useState(0);
  const [liked, setLiked] = useState(false);
  const [open, openComments] = useState(false);
  const [followers, setFollowers] = useState(props.loggedInAuthorsFollowers);
  const [friends, setFriends] = useState(props.loggedInAuthorsFriends);

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
    navigate(`/authors/${post_user_uuid}/`, { state: { refresh: true } });
  };

  // for refreshing the page of where the post card is
  const location = useLocation();
  const refreshState = () => {
    navigate(`${location.pathname}`, { state: { refresh: true } });
  };

  const sendPostLike = () => {
    let host = baseURL + "/"
    console.log("LIKE SENT WITH AUTHOR", loggedInUser);
    const postLike = {
      type: "like",
      summary: `${loggedInUser.displayName} Likes your post.`,
      author: loggedInUser,
      object: props.post.id,
    };
    if (!authorHostIsOurs(props.post.author.host) && postAuthorBaseApiURL != null){
      host = postAuthorBaseApiURL
    }
    api
      .post(`${host}authors/${post_user_uuid}/inbox`, postLike)
      .then((response) => {
        setLiked(true);
        setLikeCount((likeCount) => likeCount + 1);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // Needed to separate this from the others fetches, because
  // postAuthorNode is sometimes null. Doing it this way,
  // these fetch calls are only called once postAuthorNode changes
  // to not null. 
  useEffect(() => {
    const fetchPostAuthorData = async (ApiURL, node) => {
      await api
        .get(
          `${ApiURL}authors/${post_user_uuid}/posts/${post_id}/likes`, 
          {headers: node.headers}
        )
        .then((response) => {
          let likers = [];
          let resLikeItems = response.data.items;
          if (typeof(response.data.items) === 'undefined') {
            resLikeItems = response.data;
          }
          if (typeof(resLikeItems) !== 'undefined') {
            setLikeCount((likeCount) => resLikeItems.length);
            for (let data of resLikeItems) {
              likers.push(extractAuthorUUID(data.author.id));
              if (extractAuthorUUID(data.author.id) === loggedInUser.uuid) {
                setLiked(true);
              }
            }
          }
        })
        .catch((error) => {
          console.log(error);
      });
    await api
      .get(
        `${ApiURL}authors/${post_user_uuid}/posts/${post_id}/comments?size=10`,
        {headers: node.headers}
      )
      .then((response) => {
        let commentArray = response.data.comments;
        if (typeof(commentArray) !== 'undefined') {
          setCommentCount(commentArray.length);
          if (commentArray.length !== 0) {
            setComments(commentArray);
          }
        }
      })
      .catch((error) => {
        console.log(error);
        // TODO: If failed to fetch from theirs, fall back on ours?
      });
    }
    if (!authorHostIsOurs(props.post.author.host) && postAuthorNode !== null) {
      fetchPostAuthorData(postAuthorBaseApiURL, postAuthorNode);
    } else {
      fetchPostAuthorData(baseURL+'/', emptyNode);
    }
  }, [postAuthorNode, useLocation().state])

  const fetchNode = async (author) => {
    // fetches the node object
    await api
    .get(`${baseURL}/node/?host=${author.host}`)
    .then((response) => {
      let node = createNodeObject(response, author.host);
      setPostAuthorNode(node);
      setPostAuthorBaseAPI(node.host);
    })
    .catch((err) => {
      console.log(err.response.data);
    })
  }
  
  useEffect(() => {
    if (!authorHostIsOurs(props.post.author.host)) {
      fetchNode(props.post.author);
    }
  }, []);

  const sharePost = (post) => {
    let host = baseURL + '/';
    if (post.visibility === "PUBLIC") {
      for (let index = 0; index < followers.length; index++) {
        const follower = followers[index]
        if (!authorHostIsOurs(follower.host)) {
          api
            .get(`${baseURL}/node/?host=${follower.host}`)
            .then((response) => {
              let node = createNodeObject(response, follower.host);
              api
                .post(`${node.host}authors/${extractAuthorUUID(follower.id)}/inbox/}`, { header: node.headers }, post)
                .then((response) => {
                  console.log(response);
                })
                .catch((error) => {
                  console.log("Failed to get posts of author. " + error);
                });
          });
        } else {
          api
            .post(`${host}authors/${extractAuthorUUID(loggedInUser.id)}/inbox/}`, post)
            .then((response) => {
              console.log(response);
            })
            .catch((error) => {
              console.log("Failed to get posts of author. " + error);
            });
        }
      }
    } else if (post.visibility === "FRIENDS") {
      for (let index = 0; index < friends.length; index++) {
        const friend = friends[index]
        if (!authorHostIsOurs(friend.host)) {
          api
            .get(`${baseURL}/node/?host=${friend.host}`)
            .then((response) => {
              let node = createNodeObject(response, friend.host);
              api
                .post(`${node.host}authors/${extractAuthorUUID(friend.id)}/inbox/}`, { header: node.headers }, post)
                .then((response) => {
                  console.log(response);
                })
                .catch((error) => {
                  console.log("Failed to get posts of author. " + error);
                });
            });
        } else {
          api
            .post(`${host}authors/${extractAuthorUUID(loggedInUser.id)}/inbox/}`, post)
            .then((response) => {
              console.log(response);
            })
            .catch((error) => {
              console.log("Failed to get posts of author. " + error);
            });
        }
      }
    }
  };

  const deletePost = (uuid) => {
    api
      .delete(`${baseURL}/authors/${loggedInUser.uuid}/posts/${uuid}`)
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

  const sendCommentToInbox = (ApiURL, post_user_uuid, commentObject, node) => {
    api
      .post(`${ApiURL}authors/${post_user_uuid}/inbox`, commentObject, {
        headers: node.headers
      })
      .then((response) => {
        console.log("success send comments to inbox");
      })
      .catch((error) => {
        console.log("Failed to send comment to inbox" + error);
      });
  }

  const sendComment = (uuid) => {
    var commentObject = {};
    api
      .post(
        `${baseURL}/authors/${extractAuthorUUID(props.post.author.id)}/posts/${uuid}/comments/`,
        postComment
      )
      .then((response) => {
        

        commentObject["type"] = response.data.type;
        commentObject["comment"] = response.data.comment;
        commentObject["author"] = response.data.author;
        commentObject["id"] = response.data.id;
        commentObject["contentType"] = response.data.contentType;
        commentObject["published"] = response.data.published;
        commentObject["uuid"] = response.data.uuid;

        if (!authorHostIsOurs(props.post.author.host)) {
          sendCommentToInbox(postAuthorBaseApiURL, post_user_uuid, commentObject, postAuthorNode);
        } else {
          sendCommentToInbox(baseURL+'/', post_user_uuid, commentObject, emptyNode);
        }

        refreshState();
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
              if (loggedInUser.uuid === post_user_uuid) {
                return (
                  <div>
                    <Dropdown.Item onClick={() => setShowEditPost(true)}>
                      <MdModeEdit /> Edit Post
                    </Dropdown.Item>

                    <Dropdown.Item
                      className="delete-post"
                      onClick={() => confirmDelete(post_id)}
                    >
                      <MdDelete /> Delete Post
                    </Dropdown.Item>
                  </div>
                );
              }
            })()}
          </Dropdown.Menu>
        </Dropdown>
      </div>
    );
  }

  function FriendsIndicator() {
    return (
      props.post.visibility === "FRIENDS" ? (
        <div className="friends-indicator" style={{ marginLeft: "auto", padding: "0.3rem 1rem", marginRight: "1em" }}>
          <FaUserFriends />
          Friends-Only
        </div>
      ) : (
        <div className="friends-indicator" style={{ background: "none", marginLeft: "auto" }} />
      )
    );
  }

  function PrivateIndicator() {
    return (
      props.post.visibility === "PRIVATE" ? (
        <div className="private-indicator" style={{ marginRight: "1em", padding: "0.3rem 1rem" }}>
          <FaLock />
          Private
        </div>
      ) : (
        <div className="private-indicator" 
        style={{ background: "none", marginLeft: "none", marginRight: "none", padding: "none !important" }} />
      )
    );
  }

  function UnlistedIndicator() {
    return (
      props.post.unlisted === true ? (
        <div
          className="unlisted-indicator"
          style={{
            margin:
              props.post.visibility === "FRIENDS" || props.post.visibility === "PRIVATE"
                ? "0 1rem 0 0"
                : "0 1rem 0 auto",
          }}
        >
          <IoUnlink />
          Unlisted
        </div>
      ) : (
        <div
          className="unlisted-indicator"
          style={{
            background: "none",
            margin: "0",
            padding: "0",
          }}
        />
      )
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
        <FriendsIndicator />
        <PrivateIndicator />
        <UnlistedIndicator />
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
        {(props.post.image && (
          <img className="post-image" src={props.post.image} alt="postImage" />
        )) || (!authorHostIsOurs(props.post.author.host) && props.post.contentType.startsWith("image") 
        && isValidHTTPUrl(props.post.content) && 
        <img className="post-image" src={props.post.content} alt="postImage" />)}
        <Card.Text>
          {showContent && <ReactMarkdown>{props.post.content}</ReactMarkdown>}
        </Card.Text>
        <hr />
        <div className="like-comment-container">
          <BsFillHeartFill
            className="like-icon"
            style={{
              color:
                likeCount !== 0 && liked ? "var(--orange)" : "var(--white)",
            }}
            onClick={() => sendPostLike(post_id)}
          />

          {likeCount !== null ? likeCount : null}
          <BsFillChatFill
            className="comment-icon"
            style={{
              color: CommentCount !== 0 ? "var(--teal)" : "var(--white-teal)",
              marginLeft: "30px",
            }}
            onClick={() => openComments(!open)}
          />
          {comments.length}

          <MdShare
            className="share-icon"
            onClick={() => sharePost(props.post)}
          />
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
                onClick={() => sendComment(post_id)}
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
