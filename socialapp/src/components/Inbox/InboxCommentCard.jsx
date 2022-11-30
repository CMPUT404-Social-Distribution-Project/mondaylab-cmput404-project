import React, { useContext, useState, useEffect } from "react";
import Card from "react-bootstrap/Card";
import {useNavigate } from "react-router-dom";
import useAxios from "../../utils/useAxios";
import AuthContext from "../../context/AuthContext";
import Popup from "reactjs-popup";
import "reactjs-popup/dist/index.css";
import { BsCursorFill } from "react-icons/bs";
import "./InboxCommentCard.css";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ProfilePicture from "../ProfilePicture";
import { extractAuthorUUID } from '../../utils/utils';


export default function InboxCommentCard(props) {
  // pass in the follow request object in props
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id"); // the currently logged in author
  const api = useAxios();
  const post_uuid = props.comment.id.split("posts/")[1].split("/comments")[0];
  //const [post, setPost] = useState([]);
  const [postsArray, setPostsArray] = useState({});
  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${extractAuthorUUID(props.comment.author.id)}/`);
  };
  const postRouteChange = () => {
    var rout = props.comment.id.split("authors/")[1].split("/comments")[0];
    navigate(`/authors/${rout}`, { state: { refresh: true } });
  };

  useEffect(() => {
    api
      .get(`${baseURL}/authors/${user_id}/posts/${post_uuid}`)
      .then((response) => {
        //setPost(response.data);
        setPostsArray(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <Card className="inbox-comment-card">
      <Card.Body>
        <Row xs="auto" className="card-row align-items-center">
          <Col md="4">
            <div className="inbox-comment-card-profile" onClick={routeChange}>
              <ProfilePicture profileImage={props.comment.author.profileImage} />
              <div className="text">{props.comment.author.displayName}</div>
            </div>
          </Col>
          <Col className="col-6">
            <p className="text" style={{fontFamily:"Readex Pro Light"}}> commented on your post!</p>
          </Col>
          <Col>
            <Popup
              trigger={
                <button style={{ background: "none", border: "none" }}>
                  <BsCursorFill
                    style={{
                      color: "white",
                      marginTop: "1em",
                      marginBottom: "1em",
                      marginRight: "1em",
                    }}
                    onClick={postRouteChange}
                  />
                </button>
              }
              position="right center"
              on="hover"
              closeOnDocumentClick
              mouseLeaveDelay={100}
              mouseEnterDelay={0}
              contentStyle={{ padding: "0.5rem", backgroundColor: "var(--dark-blue)", border: "none", width: "fit-content" }}
              arrowStyle={{ color: "var(--dark-blue)", stroke: "none" }}
              arrow={true}
            >
              <span> View Post </span>
            </Popup>
          </Col>
        </Row>
      </Card.Body>
      <div className="inbox-comment-card-comment">
        {props.comment.comment}
      </div>
    </Card>
  );
}
