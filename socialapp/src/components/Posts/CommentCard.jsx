import { React, useState, useContext, useEffect } from "react";
import { Card } from "react-bootstrap";
import "./CommentCard.css";
import { useNavigate } from "react-router-dom";
import { BsFillHeartFill } from "react-icons/bs";
import AuthContext from "../../context/AuthContext";
import { extractAuthorUUID } from "../../utils/utils";
import useAxios from "../../utils/useAxios";
import ProfilePicture from "../ProfilePicture";
import ReactMarkdown from "react-markdown";

export default function CommentCard(props) {
  const [liked, setLiked] = useState(props.liked);
  const { baseURL } = useContext(AuthContext);
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const api = useAxios();

  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${extractAuthorUUID(props.author.id)}/`, {
      state: { refresh: true },
    });
  };

  useEffect(() => {
    setLiked(props.liked);
  }, [props.liked]);

  const sendLike = () => {
    const postLike = {
      type: "like",
      summary: `${loggedInUser.displayName} Likes your post.`,
      author: loggedInUser,
      object: props.comment.id,
    };
    api
      .post(
        `${baseURL}/authors/${extractAuthorUUID(props.author.id)}/inbox/`,
        postLike
      )
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

  return (
    <Card className="comment-card">
      <Card.Body style={{ width: "auto", display: "flex" }}>
        <div className="comment-author-container" onClick={routeChange}>
          <ProfilePicture profileImage={props.author.profileImage} />
          <div className="comment-author">{props.author.displayName}</div>
        </div>
        <ReactMarkdown
          className="comment-content"
          children={props.comment.comment}
          components={{
            img: ({ node, ...props }) => (
              <img style={{ maxWidth: "50%", maxHeight: "20rem" }} {...props} />
            ),
          }}
        />
      </Card.Body>
      <BsFillHeartFill
        className="comment-like-icon"
        style={{
          color: liked ? "var(--orange)" : "var(--white-teal)",
        }}
        onClick={() => sendLike()}
      />
    </Card>
  );
}
