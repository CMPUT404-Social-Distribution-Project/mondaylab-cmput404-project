import React, { useContext, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Dropdown } from "react-bootstrap";
import { BiDotsVerticalRounded } from "react-icons/bi";
import { MdModeEdit, MdDelete, MdShare } from "react-icons/md";
import Card from "react-bootstrap/Card";
import AuthContext from "../../context/AuthContext";
import "./ExplorePostCard.css";
import useAxios from "../../utils/useAxios";
import { useEffect } from "react";
import EditPost from "./EditPost";
import { BsFillHeartFill, BsCursorFill } from "react-icons/bs";
import { useNavigate, useLocation } from "react-router-dom";
import Popup from "reactjs-popup";
import "reactjs-popup/dist/index.css";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { confirmAlert } from "react-confirm-alert";
import {
  authorHostIsOurs,
  isValidHTTPUrl,
  urlContainsOurHost,
  extractAuthorUUID,
  extractPostUUID,
} from "../../utils/utils";
import ProfilePicture from "../ProfilePicture";
import { Buffer } from 'buffer';
import { toast } from 'react-toastify';
import PublishedAgo from "./PublishedAgo";

export default function PostCard(props) {
  const user_id = localStorage.getItem("user_id");
  const post_id = extractPostUUID(props.post.id);
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const post_user_uuid = extractAuthorUUID(props.post.author.id);
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const [showEditPost, setShowEditPost] = useState(false);
  const api = useAxios();
  const [likeCount, setLikeCount] = useState(0);
  const [liked, setLiked] = useState(false);
  const [followers, setFollowers] = useState(props.loggedInAuthorsFollowers);
  const [friends, setFriends] = useState(props.loggedInAuthorsFriends);
  const loggedInAuthorsLiked = props.loggedInAuthorsLiked;
  const [postImage, setPostImage] = useState(props.post.image);

  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${post_user_uuid}/`, { state: { refresh: true } });
  };

  const location = useLocation();
  const refreshState = () => {
    navigate(`${location.pathname}`, { state: { refresh: true } });
  };

  const [showContent, setShowContent] = useState(() => {
    if (props.post.contentType.startsWith("image")) {
      return false;
    } else {
      return true;
    }
  });
  const postRouteChange = () => {
    navigate(`/authors/${post_user_uuid}/posts/${post_id}`);
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
    // check if post is liked by logged in author
    if (loggedInAuthorsLiked && typeof loggedInAuthorsLiked !== "undefined") {
      for (let data of loggedInAuthorsLiked) {
        if (data.object === props.post.id) {
          setLiked(true);
          break;
        }
      }
    }
  }, [loggedInAuthorsLiked]);

  useEffect(() => {
    const fetchImage = async () => {
      await api
        .get(`${props.post.image}`, { responseType: "arraybuffer" })
        .then((res) => {
          const data = `data:${
            res.headers["content-type"]
          };base64,${Buffer.from(res.data, "binary").toString("base64")}`;
          setPostImage(data);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    if (props.post.image && urlContainsOurHost(props.post.image)) {
      fetchImage();
    }
  });

  const sharePost = (post) => {
    if (post.visibility === "PUBLIC" || post.visibility === "FRIENDS") {
      let successes = 0;
      let requests = [];
      for (let index = 0; index < followers.length; index++) {
        const follower = followers[index];
        requests.push(api.post(`${baseURL}/authors/${extractAuthorUUID(follower.id)}/inbox/`, post));
      }
      Promise.allSettled(requests)
      .then((results) => {
        results.forEach((response) => {
          if (response.status === "fulfilled") {
            successes++;
          }
        })
        toast(`Successfully sent post to ${successes} of ${followers.length} followers.`, {
          theme: "dark",
          hideProgressBar: false,
          autoClose: 2000
        })
      })
      .catch((errors) => {
        errors.forEach((err) => {
          console.log(err);
        })
      })
    }
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
                      onClick={() => confirmDelete(props.post.uuid)}
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

  return (
    <Card className="post-card-explore">
      <Card.Header>
        <div className="post-author" onClick={routeChange}>
          <ProfilePicture profileImage={props.post.author.profileImage} />
          <div className="post-author-name">
            {props.post.author.displayName}
          </div>
        </div>
        <PublishedAgo explore={true} published={props.post.published} />
        <PostOptions />
        {showEditPost && (
          <EditPost
            show={showEditPost}
            onHide={() => setShowEditPost(false)}
            post={props.post}
          />
        )}
      </Card.Header>
      <Card.Img variant="top" src="" />
      <Card.Body>
        <Card.Title>
          <ReactMarkdown>{props.post.title}</ReactMarkdown>
        </Card.Title>
        <Card.Text>
          {(postImage && (
            <img
              className="post-image"
              src={postImage}
              alt="postImage"
              style={{ maxWidth: "100%", maxHeight: "100%" }}
            />
          )) ||
            (!authorHostIsOurs(props.post.author.host) &&
              props.post.contentType.startsWith("image") &&
              isValidHTTPUrl(props.post.content) && (
                <img
                  className="post-image"
                  src={props.post.content}
                  alt="postImage"
                  style={{ maxWidth: "100%", maxHeight: "100%" }}
                />
              ))}
          {!postImage && showContent ? (
            <ReactMarkdown
              components={{
                img: ({ node, ...props }) => (
                  <img style={{ maxWidth: "100%" }} {...props} />
                ),
              }}
            >
              {props.post.content}
            </ReactMarkdown>
          ) : null}
        </Card.Text>

        <hr />
        <Row>
          <Col>
            <div>
              <BsFillHeartFill
                className="like-icon"
                style={{ color: liked ? "var(--orange)" : "var(--white-teal)" }}
                onClick={() => sendPostLike()}
              />
            </div>
          </Col>
          <Col style={{ display: "flex", height: "fit-content" }}>
            <Popup
              trigger={
                <button
                  style={{
                    background: "none",
                    border: "none",
                    marginLeft: "auto",
                    padding: "0.5rem",
                    width: "2rem",
                    height: "2rem",
                  }}
                >
                  <BsCursorFill
                    style={{ color: "var(--white-teal)", verticalAlign: "top" }}
                    onClick={postRouteChange}
                  />
                </button>
              }
              position="bottom center"
              on="hover"
              closeOnDocumentClick
              mouseLeaveDelay={300}
              mouseEnterDelay={0}
              arrow={true}
              contentStyle={{
                backgroundColor: "var(--dark-blue)",
                border: "none",
                width: "fit-content",
                padding: "0.5em",
              }}
              arrowStyle={{ color: "var(--dark-blue)", stroke: "none" }}
            >
              <span style={{ fontSize: "0.8rem" }}> View Post </span>
            </Popup>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
