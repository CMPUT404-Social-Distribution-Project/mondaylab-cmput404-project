import React, { useEffect, useState, useContext } from "react";
import Button from "react-bootstrap/Button";
import AuthContext from "../../context/AuthContext";
import useAxios from "../../utils/useAxios";
import { useParams, useLocation } from "react-router-dom";
import { authorHostIsOurs, emptyNode } from "../../utils/utils";

// function authorInArray(id, array) {
//   // checks if the given author id is in the array
//   var i;
//   for (i = 0; i < array.length; i++) {
//     if (array[i].id === id) {
//       return true;
//     }
//   }
//   return false;
// }

export default function FollowButton(props) {
  // if not the current user, make the follow button visible
  const [isNotCurrentUser, setIsNotCurrentUser] = useState(true);
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const api = useAxios(); // use this to add authorization header
  const currentAuthor = JSON.parse(localStorage.getItem("authTokens")).user; // the currently logged in author as an object
  const { author_id } = useParams(); // gets the author id in the url
  // Check if the currently logged in user is following the author they're viewing
  const [isFollowing, setIsFollowing] = useState(false);
  // set the follow state
  const [followState, setFollowState] = useState("notFollowing");

  useEffect(() => {
    if (currentAuthor.uuid === author_id) {
      // if the current user (user_id) has the same id in the url, don't show follow button
      setIsNotCurrentUser(false);
    }
  }, [isNotCurrentUser, useLocation().state]);

  useEffect(() => {
    const following = async (ApiURL, node) => {
      await api
        .get(`${ApiURL}authors/${author_id}/followers/${currentAuthor.uuid}`,
         { header: node.headers }
        )
        .then((response) => {
          if (response.data) {
            setIsFollowing(response.data);
            setFollowState("following");
          } else {
            setFollowState("notFollowing");
          }
        })
        .catch((error) =>{
          console.log(
            "Failed to get check if current author is following ", error.response
          );
        })
    };
    if (!authorHostIsOurs(props.authorViewing.host) && props.authorBaseApiURL !== null) {
      following(props.authorBaseApiURL, props.authorNode);
    } else {
      following(baseURL+'/', emptyNode);
    }
  }, [isFollowing, useLocation().state]);

  const handleClick = () => {
    if (followState === "notFollowing") {
      setFollowState("followSent");
      // Send a friend request object to the inbox of the author we're viewing
      api
        .post(`${props.authorBaseApiURL}authors/${author_id}/inbox/`, {
          type: "follow",
          summary: `${currentAuthor.displayName} wants to follow ${props.authorViewing.displayName}`,
          actor: currentAuthor,
          object: props.authorViewing,
        },
        {headers: props.authorNode.headers}
        )
        .then((response) => {
          console.log("Success sending a friend request: " + response);
        })
        .catch((error) => {
          setFollowState("notFollowing");
      });
    } else if (followState === "following") {
      // if we're already following, clicking will unfollow
      api
        .delete(
          `${props.authorBaseApiURL}authors/${author_id}/followers/${currentAuthor.uuid}`,
          {headers: props.authorNode.headers}
        )
        .then((response) => {
          console.log(
            "Success removing current author from viewing author's followers: " +
              response
          );
          setFollowState("notFollowing");
        })
        .catch((error) => {
          console.log("Failed to unfollow: " + error);
      });
    }
  };

  if (currentAuthor.uuid === props.authorViewing.uuid) {
    // don't show if viewing oneself's profile
    return <div className="empty-space" style={{ width: "3em" }} />;
  } else {
    return (
      <Button
        id="followButton"
        variant="primary"
        disabled={followState === "followSent"}
        onClick={followState !== "followSent" ? handleClick : null}
        style={{
          backgroundColor:
            followState === "following" ? "var(--orange)" : "var(--teal)",
        }}
      >
        {followState === "following" ? "Following" : ""}
        {followState === "followSent" ? "Sent" : ""}
        {followState === "notFollowing" ? "Follow" : ""}
      </Button>
    );
  }
}
