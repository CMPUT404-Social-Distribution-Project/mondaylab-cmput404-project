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
import {
  extractAuthorUUID,
  extractPostUUID,
  authorHostIsOurs,
  isValidHTTPUrl,
} from "../../utils/utils";
import ProfilePicture from "../ProfilePicture";
import remarkGfm from "remark-gfm";
import PulseLoader from "react-spinners/PulseLoader";

export default function PostCard(props) {
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const post_user_uuid = extractAuthorUUID(props.post.author.id);
  const post_id = extractPostUUID(props.post.id);
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const [nextUrl, setNextUrl] = useState();
  const [postComment, setPostComment] = useState({
    comment: "",
    type: "comment",
    contentType: "text/markdown",
    author: loggedInUser,
    object: props.post.id,
  });
  const [comments, setComments] = useState([]);
  const [showEditPost, setShowEditPost] = useState(false);
  const api = useAxios();
  const [likeCount, setLikeCount] = useState(null);
  const [commentCount, setCommentCount] = useState(props.post.count);
  const [liked, setLiked] = useState(false);
  const [open, openComments] = useState(false);
  const [followers, setFollowers] = useState(props.loggedInAuthorsFollowers);
  const [loadingComments, setLoadingComments] = useState(false);

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
    const postLike = {
      type: "like",
      summary: `${loggedInUser.displayName} Likes your post.`,
      author: loggedInUser,
      object: props.post.id,
    };
    api
      .post(`${baseURL}/authors/${post_user_uuid}/inbox/`, postLike)
      .then((response) => {
        setLiked(true);
        if (
          props.post.visibility === "FRIENDS" ||
          props.post.author.id === loggedInUser.id
        ) {
          setLikeCount((likeCount) => likeCount + 1);
        }

        // Need this for checking if author liked remote post or not.
        // Since when sending a like object to remote host's inbox,
        // the like object is created in their DB but not ours. So
        // create a like object in ours as well.
        api
          .post(`${baseURL}/authors/${loggedInUser.uuid}/liked`, postLike)
          .catch((error) => {
            console.log(
              "Failed to create backup like object",
              error.response.data
            );
          });
      })
      .catch((error) => {
        console.log("Failed to send like to inbox", error.response);
      });
  };

  useEffect(() => {
    const fetchPostAuthorData = async () => {
      await api
        .get(`${baseURL}/authors/${post_user_uuid}/posts/${post_id}/likes/`)
        .then((response) => {
          let resLikeItems = response.data.items;
          if (typeof response.data.items === "undefined") {
            resLikeItems = response.data;
          }
          if (typeof resLikeItems !== "undefined") {
            setLikeCount((likeCount) => resLikeItems.length);
          }
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response.data);
          }
        });
      await api
        .get(
          `${baseURL}/authors/${post_user_uuid}/posts/${post_id}/comments/?size=10`
        )
        .then((response) => {
          let commentArray = response.data.comments;
          if (typeof commentArray !== "undefined") {
            setNextUrl(response.data.next);
            if (commentArray.length !== 0) {
              setComments(commentArray);
              if (commentCount < commentArray.length) {
                setCommentCount(commentArray.length);
              }
            }
          }
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response.data);
          }
        });
    };
    fetchPostAuthorData();
  }, [useLocation().state]);

  useEffect(() => {
    // check if post is liked by logged in author
    if (typeof props.loggedInAuthorsLiked !== "undefined") {
      for (let data of props.loggedInAuthorsLiked) {
        if (data.object === props.post.id) {
          setLiked(true);
          break;
        }
      }
    }
  }, [props.loggedInAuthorsLiked]);

  const sendPostToAuthorInbox = (author, post) => {
    api
      .post(`${baseURL}/authors/${extractAuthorUUID(author.id)}/inbox/`, post)
      .then((response) => {
        console.log("Success sending to author's inbox", response);
      })
      .catch((error) => {
        console.log("Failed to send post to inbox of author", error.response);
      });
  };

  const sharePost = (post) => {
    if (post.visibility === "PUBLIC" || post.visibility === "FRIENDS") {
      for (let index = 0; index < followers.length; index++) {
        const follower = followers[index];
        sendPostToAuthorInbox(follower, post);
      }
    }
  };

  const deletePost = (uuid) => {
    api
      .delete(`${baseURL}/authors/${loggedInUser.uuid}/posts/${uuid}`)
      .then((response) => {
        refreshState();
      })
      .catch((error) => {
        alert(`Something went wrong posting! \n Error: ${error}`);
        console.log(error);
      });
  };

  const confirmDelete = (uuid) => {
    confirmAlert({
      title: "Confirm to submit",
      message: "Are you sure you want to delete this post?",
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

  const sendCommentToInbox = (post_user_uuid, commentObject) => {
    api
      .post(`${baseURL}/authors/${post_user_uuid}/inbox/`, commentObject)
      .then((response) => {
        console.log("success send comments to inbox");
      })
      .catch((error) => {
        alert("Failed to send comment to inbox of post's author");
      });
  };

  const sendComment = (e) => {
    e.preventDefault();
    var commentObject = {};
    // otherwise create the comment on our local post, then send comment to inbox of post's author
    api
      .post(
        `${baseURL}/authors/${extractAuthorUUID(
          props.post.author.id
        )}/posts/${post_id}/comments/`,
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
        commentObject["object"] = props.post.id;
        console.log("Comment obj is", response.data);

        sendCommentToInbox(post_user_uuid, commentObject);

        setPostComment({ ...postComment, comment: "" });
        e.target.reset();
        refreshState();
      })
      .catch((error) => {
        alert(`Something went wrong posting! \n Error: ${error}`);
        console.log(error);
      });
  };

  const paginationHandler = (url) => {
    setLoadingComments(true);
    api
    .get(url)
    .then((response) => {
      setNextUrl(response.data.next);
      var temp = [...comments, ...response.data.comments]
      setComments(temp);
      if (commentCount < temp.length) {
        setCommentCount(temp.length);
      }
      setLoadingComments(false);
    })
    .catch((error) => {
      setLoadingComments(false);
      console.log("pagination", error);
    })

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
              if (
                loggedInUser.uuid === post_user_uuid &&
                props.post.visibility === "PUBLIC"
              ) {
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
              } else if (loggedInUser.uuid === post_user_uuid) {
                // Shouldn't be allowed to edit PRIVATE or FRIENDS posts, as they are already sent
                return (
                  <div>
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
    return props.post.visibility === "FRIENDS" ? (
      <div
        className="friends-indicator"
        style={{
          marginLeft: "auto",
          padding: "0.3rem 1rem",
          marginRight: "1em",
        }}
      >
        <FaUserFriends />
        Friends-Only
      </div>
    ) : (
      <div
        className="friends-indicator"
        style={{ background: "none", marginLeft: "auto" }}
      />
    );
  }

  function PrivateIndicator() {
    return props.post.visibility === "PRIVATE" ? (
      <div
        className="private-indicator"
        style={{ marginRight: "1em", padding: "0.3rem 1rem" }}
      >
        <FaLock />
        Private
      </div>
    ) : (
      <div
        className="private-indicator"
        style={{
          background: "none",
          marginLeft: "none",
          marginRight: "none",
          padding: "none !important",
        }}
      />
    );
  }

  function UnlistedIndicator() {
    return props.post.unlisted === true ? (
      <div
        className="unlisted-indicator"
        style={{
          margin:
            props.post.visibility === "FRIENDS" ||
            props.post.visibility === "PRIVATE"
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
    );
  }

  return (
    <Card className="post-card">
      <Card.Header>
        <div className="post-author" onClick={routeChange}>
          <ProfilePicture profileImage={props.post.author.profileImage} />
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
        <Card.Title>{props.post.title}</Card.Title>
        {(props.post.image && (
          <img className="post-image" src={props.post.image} alt="postImage" />
        )) ||
          (!authorHostIsOurs(props.post.author.host) &&
            props.post.contentType.startsWith("image") &&
            isValidHTTPUrl(props.post.content) && (
              <img
                className="post-image"
                src={props.post.content}
                alt="postImage"
              />
            ))}
        <div className="card-text">
          {showContent && (
            <ReactMarkdown
              children={props.post.content}
              remarkPlugins={[remarkGfm]}
              components={{
                img: ({ node, ...props }) => (
                  <img style={{ maxWidth: "100%" }} {...props} />
                ),
              }}
            ></ReactMarkdown>
          )}
        </div>
        <hr />
        <div className="like-comment-container">
          <BsFillHeartFill
            className="like-icon"
            style={{
              color:
                likeCount !== 0 && liked
                  ? "var(--orange)"
                  : "var(--white-teal)",
            }}
            onClick={() => sendPostLike(post_id)}
          />

          {likeCount !== null ? likeCount : null}
          <BsFillChatFill
            className="comment-icon"
            style={{
              color: commentCount !== 0 ? "var(--teal)" : "var(--white-teal)",
              marginLeft: "30px",
            }}
            onClick={() => openComments(!open)}
          />
          {commentCount}

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
                {comments.length === 0 ? (
                  <p>No Comments</p>
                ) : (
                  comments.map((comment, i) => (
                    <CommentCard
                      key={i}
                      author={comment.author}
                      comment={comment}
                      liked={() => {
                        for (let likedObj of props.loggedInAuthorsLiked) {
                          if (likedObj.object === comment.id) {
                            return true;
                          }
                        }
                        return false;
                      }}
                    />
                  ))
                )}
                {loadingComments && <PulseLoader className="comments-loader" color="var(--teal)"/>}
                {nextUrl && (
                  <button
                    className="load-more-comments-button"
                    onClick={() => paginationHandler(nextUrl)}
                  >
                    Load More Comments
                  </button>
                )}
              </div>
            </div>
          ) : null}
        </div>
        <div className="comments-container">
          <Form className="input-comment mb-3" onSubmit={sendComment}>
            <Form.Control
              placeholder="Comment"
              aria-label="Comment"
              onChange={(e) =>
                setPostComment({ ...postComment, comment: e.target.value })
              }
            ></Form.Control>
            <Button
              style={{
                borderRadius: "1.5rem",
                color: "black",
                backgroundColor: "#BFEFE9",
              }}
              type="submit"
            >
              Send
            </Button>
          </Form>
        </div>
      </Card.Body>
    </Card>
  );
}
