import { React, useState, useContext, useEffect } from "react";
import { Card } from "react-bootstrap";
import "./CommentCard.css";
import { useNavigate } from "react-router-dom";
import { BsFillHeartFill } from "react-icons/bs";
import AuthContext from "../../context/AuthContext";
import { extractAuthorUUID, authorHostIsOurs, emptyNode } from "../../utils/utils";
import useAxios from "../../utils/useAxios";
import ProfilePicture from "../ProfilePicture";

export default function CommentCard(props) {
  const [liked, setLiked] = useState(props.liked);
  const [node, setNode] = useState(emptyNode);
  const { baseURL } = useContext(AuthContext);
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const api = useAxios();

  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${extractAuthorUUID(props.author.id)}/`, { state: { refresh: true } });
  };

  useEffect(() => {
    setLiked(props.liked);
    setNode(props.node);
  }, [props.node, props.liked])


  const sendLike = () => {
    let host = baseURL + "/";
    const postLike = {
      type: "like",
      summary: `${loggedInUser.displayName} Likes your post.`,
      author: loggedInUser,
      object: props.comment.id,
    };
    if (!authorHostIsOurs(props.author.host) && props.node.host != null){
      host = props.node.host;
    }
    api
      .post(`${host}authors/${extractAuthorUUID(props.author.id)}/inbox/`, postLike, {headers: node.headers})
      .then((response) => {
        setLiked(true);

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

  return (
    <Card className="comment-card">
      <Card.Body style={{ width: "auto", display: "flex" }}>
        <div className="comment-author-container" onClick={routeChange}>
          <ProfilePicture profileImage={props.author.profileImage} />
          <div className="comment-author">{props.author.displayName}</div>
        </div>
        <div className="comment-content">{props.comment.comment}</div>
      </Card.Body>
      <BsFillHeartFill
            className="comment-like-icon"
            style={{
              color:
                liked ? "var(--orange)" : "var(--white-teal)",
            }}
            onClick={() => sendLike()}
          />
    </Card>
  );
}
