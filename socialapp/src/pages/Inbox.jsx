import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import AuthContext from "../context/AuthContext";
import "./pages.css";
import FollowRequestCard from "../components/Inbox/FollowRequestCard";
import LikeCard from "../components/Inbox/LikeCard";
import PostCard from "../components/Posts/PostCard";
import InboxCommentCard from "../components/Inbox/InboxCommentCard";
import Tab from "react-bootstrap/Tab";
import { BsFillTrashFill } from "react-icons/bs";
import { confirmAlert } from "react-confirm-alert";
import "react-confirm-alert/src/react-confirm-alert.css";
import Popup from "reactjs-popup";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Toast from "react-bootstrap/Toast";
import Nav from "react-bootstrap/Nav";
import { useLocation } from "react-router-dom";
import "./Inbox.css";

export default function Inbox() {
  const [inboxItems, setInboxItems] = useState([]);
  const [posts, setPosts] = useState([]);
  const [postNum, setPostNum] = useState(0);
  const [likeNum, setLikeNum] = useState(0);
  const [commentNum, setCommentNum] = useState(0);
  const [followNum, setFollowNum] = useState(0);
  const [followRequests, setFollowRequests] = useState([]);
  const [likes, setLikes] = useState([]);
  const [comments, setComments] = useState([]);
  const { baseURL } = useContext(AuthContext) || {}; // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id"); // the currently logged in author
  const [followers, setFollowers] = useState([]);
  const [friends, setFriends] = useState([]);
  const [liked, setLiked] = useState([]);
  const api = useAxios();
  const [show, setShow] = useState(false);

  useEffect(() => {
    const fetchLoggedInAuthorData = async () => {
      await api
      .get(`${baseURL}/authors/${user_id}/followers/`)
      .then((response) => {
        setFollowers(response.data.items);
      })
      .catch((error) => {
        console.log(error);
      });
      await api
        .get(`${baseURL}/authors/${user_id}/friends/`)
        .then((response) => {
          setFriends(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(
          `${baseURL}/authors/${user_id}/liked`
        )
        .then((response) => {
          setLiked(response.data.items);
        })
        .catch((error) => {
          console.log(error);
      });
    }
    fetchLoggedInAuthorData();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      await api
        .get(`${baseURL}/authors/${user_id}/inbox/all`)
        .then((response) => {
          // Since clicking inbox icon in sidebar recalls this function,
          // all these states need to be reset, otherwise one could
          // infinitely click on inbox to add a lot duplicate posts/likes/etc.
          setPostNum(0);
          setLikeNum(0);
          setCommentNum(0);
          setFollowNum(0);
          setPosts([]);
          setLikes([]);
          setComments([]);
          setFollowRequests([]);
          setInboxItems(response.data.items);
          for (let i = 0; i < response.data.items.length; i++) {
            if (response.data.items[i].type.toLowerCase() === "follow") {
              setFollowNum((followNum) => followNum + 1);
              setFollowRequests((followRequests) => [
                ...followRequests,
                response.data.items[i],
              ]);
            } else if (response.data.items[i].type.toLowerCase() === "like") {
              setLikeNum((likeNum) => likeNum + 1);
              setLikes((likes) => [...likes, response.data.items[i]]);
            } else if (
              response.data.items[i].type.toLowerCase() === "comment"
            ) {
              if (response.data.items[i].author != null) {
                setCommentNum((commentNum) => commentNum + 1);
                setComments((comments) => [
                  ...comments,
                  response.data.items[i],
                ]);
              }
            } else if (response.data.items[i].type.toLowerCase() === "post") {
              setPostNum((postNum) => postNum + 1);
              setPosts((posts) => [response.data.items[i], ...posts]);
            }
          }

        })
        .catch((error) => {
          console.log("Failed to get inbox of author. " + error);
        });
    };
    fetchData();
  }, [useLocation().state]);

  const clearInbox = () => {
    confirmAlert({
      title: "Clear inbox?",
      buttons: [
        {
          label: "Yes",
          className: "yes-button",
          onClick: () => deleteInbox(),
        },
        {
          className: "no-button",
          label: "No",
        },
      ],
    });
  };
  
  const deleteInbox = () => {
    api
      .delete(`${baseURL}/authors/${user_id}/inbox/`)
      .then(
        (response) => setShow(true),
        setPosts([]),
        setComments([]),
        setLikes([]),
        setFollowRequests([]),
        setPostNum(0),
        setLikeNum(0),
        setCommentNum(0),
        setFollowNum(0),
      )
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="inbox-container">
      <Row xs="auto">
        <Col>
          <h1>Inbox</h1>
        </Col>
        <Col>
          <Popup
            trigger={
              <div>
                <BsFillTrashFill
                  style={{
                    color: "var(--orange)",
                    marginTop: "1em",
                    marginBottom: "1em",
                    marginRight: "1em",
                  }}
                  onClick={clearInbox}
                />
              </div>
            }
            position="right center"
            on="hover"
            closeOnDocumentClick
            contentStyle={{ padding: "0.5rem", "background-color": "var(--dark-blue)", border: "none", width: "fit-content" }}
            arrowStyle={{ color: "var(--dark-blue)", stroke: "none" }}
          >
            <span> Clear Inbox </span>
          </Popup>
        </Col>
      </Row>

      <div className="inbox-container">
        <Tab.Container id="left-tabs-example" defaultActiveKey="post">
          <Row>
            <Row>
              <Nav
                variant="pills"
                id="inbox-tab-row"
                justify
                fill
              >
                <Nav.Item>
                  <Nav.Link eventKey="post">Post {postNum}</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="like">Like {likeNum}</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="comment">Comment {commentNum}</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="follow">
                    Follow Request {followNum}
                  </Nav.Link>
                </Nav.Item>
              </Nav>
            </Row>
            <Col>
              <Tab.Content>
                <Tab.Pane eventKey="post">
                  {typeof posts !== "undefined" ? (
                    posts.length !== 0 ? (
                      posts.map((item, i) => <PostCard loggedInAuthorsLiked={liked} loggedInAuthorsFollowers={followers} loggedInAuthorsFriends={friends} post={item} key={i}/>)
                    ) : (
                      <h4>No posts yet! </h4>
                    )
                  ) : (
                    <h4>No posts yet! </h4>
                  )}
                </Tab.Pane>
                <Tab.Pane eventKey="like">
                  {typeof likes !== "undefined" ? (
                    likes.length !== 0 ? (
                      likes.map((item, i) => <LikeCard like={item} key={i}/>)
                    ) : (
                      <h4>No like yet! </h4>
                    )
                  ) : (
                    <h4>No like yet! </h4>
                  )}
                </Tab.Pane>
                <Tab.Pane eventKey="comment">
                  {typeof comments !== "undefined" ? (
                    comments.length !== 0 ? (
                      comments.map((item, i) => (
                        <InboxCommentCard comment={item} key={i}/>
                      ))
                    ) : (
                      <h4>No comments yet! </h4>
                    )
                  ) : (
                    <h4>No comments yet! </h4>
                  )}
                </Tab.Pane>
                <Tab.Pane eventKey="follow">
                  {typeof followRequests !== "undefined" ? (
                    followRequests.length !== 0 ? (
                      followRequests.map((item, i) => (
                        <FollowRequestCard followRequest={item} key={i}/>
                      ))
                    ) : (
                      <h4>No follow requests yet! </h4>
                    )
                  ) : (
                    <h4>No follow requests yet! </h4>
                  )}
                </Tab.Pane>
              </Tab.Content>
            </Col>
          </Row>
        </Tab.Container>
      </div>
      <Toast onClose={() => setShow(false)} show={show} delay={1500} autohide>
        <Toast.Header>
          <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
          <strong className="me-auto">Bootstrap</strong>
        </Toast.Header>
        <Toast.Body>Cleared inbox successfully</Toast.Body>
      </Toast>
    </div>
  );
}
