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
import { authorHostIsOurs, extractAuthorUUID, extractPostUUID, createNodeObject, emptyNode } from "../../utils/utils";

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

  // node
  const [postAuthorNode, setPostAuthorNode] = useState(null);     // the node object of post's author
  const [postAuthorBaseApiURL, setPostAuthorBaseAPI] = useState("");
  
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
    var rout = props.post.id.split("authors/")[1];
    navigate(`/authors/${rout}`);
  };

  const sendPostLike = () => {
    let host = baseURL + "/";
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

        // Need this for checking if author liked remote post or not.
        // Since when sending a like object to remote host's inbox,
        // the like object is created in their DB but not ours. So 
        // create a like object in ours as well.
        api
          .post(`${baseURL}/authors/${loggedInUser.uuid}/liked`, postLike)
          .catch((error) => {
            console.log("Failed to create backup like object", error.response.data);
          });
      })
      .catch((error) => {
        console.log("Failed to send like to inbox", error.response);
      });
  };

  useEffect(() => {
    if (!authorHostIsOurs(props.post.author.host)) {
      const fetchNode = async () => {
        // fetches the node object
        await api
        .get(`${baseURL}/node/?host=${props.post.author.host}`)
        .then((response) => {
          let node = createNodeObject(response, props.post.author);
          setPostAuthorNode(node);
          setPostAuthorBaseAPI(node.host);
        })
        .catch((err) => {
          console.log(err.response.data);
        })
      }
      fetchNode();
    }
  }, []);

  // Checks the logged in user's liked objects,
  // if it matches this post's ID, then set liked to be true.
  useEffect(() => {
    const fetchLoggedUsersLiked = async () => {
      await api
        .get(
          `${baseURL}/authors/${loggedInUser.uuid}/liked`
        )
        .then((response) => {
          let resLikedItems = response.data.items;
          if (typeof(response.data.items) === 'undefined') {
            resLikedItems = response.data;
          }
          if (typeof(resLikedItems) !== 'undefined') {
            // console.log(props.post.id);

            for (let data of resLikedItems) {
              if (data.object === props.post.id) {
                setLiked(true);
                break;
              }
            }
          }
        })
        .catch((error) => {
          console.log(error);
      });
    }
    fetchLoggedUsersLiked();
  }, [])

  const sendPostToAuthorInbox = (author, post) => {
    if (!authorHostIsOurs(author.host)) {
      api
        .get(`${baseURL}/node/?host=${author.host}`)
        .then((response) => {
          let node = createNodeObject(response, author);
          api
            .post(`${node.host}authors/${extractAuthorUUID(author.id)}/inbox`, { header: node.headers }, post)
            .then((response) => {
              console.log("Success sending to author's inbox", response);
            })
            .catch((error) => {
              console.log("Failed to send post to inbox of author", error.response);
            });
      });
    } else {
      api
        .post(`${baseURL}/authors/${extractAuthorUUID(author.id)}/inbox`, post)
        .then((response) => {
          console.log("Success sending to author's inbox", response);
        })
        .catch((error) => {
          console.log("Failed to send post to inbox of author", error.response);
        });
    }
  }

  const sharePost = (post) => {
    if (post.visibility === "PUBLIC") {
      for (let index = 0; index < followers.length; index++) {
        const follower = followers[index];
        sendPostToAuthorInbox(follower, post);
      };
    } else if (post.visibility === "FRIENDS") {
      for (let index = 0; index < friends.length; index++) {
        const friend = friends[index];
        sendPostToAuthorInbox(friend, post);
      };
    };
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
      .delete(`${baseURL}/authors/${extractAuthorUUID(loggedInUser.id)}/posts/${uuid}`)
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
                    )
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
          <div className="profile-pic-post">
            <img src={props.post.author.profileImage} alt="profilePic" />
          </div>
          <div className="post-author-name">
            {props.post.author.displayName}
          </div>
        </div>
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
          {props.post.image ? (
            <img
              className="post-image"
              src={props.post.image}
              alt="postImage"
              style={{ height: "100%", width: "100%", objectfit: "contain" }}
            />
          ) : showContent ? (
            <ReactMarkdown>{props.post.content}</ReactMarkdown>
          ) : null}
        </Card.Text>

        <hr />
        <Row>
          <Col>
            <div>
              <BsFillHeartFill
                className="like-icon"
                style={{color: liked ? "var(--orange)": "var(--white)",}}
                onClick={() => sendPostLike(props.post.uuid)}
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
              contentStyle={{ backgroundColor: "var(--dark-blue)", border: "none", width: "fit-content", padding: "0.5em" }}
              arrowStyle={{ color: "var(--dark-blue)", stroke: "none" }}
            >
              <span style={{ fontSize: "0.8rem"}}> View Post </span>
            </Popup>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
