import React, { useEffect, useState, useContext } from "react";
import Button from "react-bootstrap/Button";
import AuthContext from "../../context/AuthContext";
import useAxios from "../../utils/useAxios";
import { useParams, useLocation } from "react-router-dom";

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
    // first fetch the author
    const fetchAuthor = async () => {
      await axios
        .get(`${baseURL}/authors/${author_id}/`)
        .then((response) => {
          setAuthor(response.data);
          fetchNode(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
    fetchAuthor();
  }, [useLocation().state, dir])

  const fetchNode = async (author) => {
    // fetches the node object
    await api
      .get(`${baseURL}/node/?host=${author.host}`)
      .then((response) => {
        let node = createNodeObject(response, author.host);
        setAuthorNode(node);
        setAuthorBaseAPI(node.host);
      })
      .catch((err) => {
        console.log(err.response.data);
      })
  }

  useEffect(() => {
    if (currentAuthor.uuid === author_id) {
      // if the current user (user_id) has the same id in the url, don't show follow button
      setIsNotCurrentUser(false);
    }
  }, [isNotCurrentUser, useLocation().state]);

  useEffect(() => {
    const following = async () => {
      if (!authorHostIsOurs(author.host) && authorBaseApiURL !== null) {
        await api
          .get(`${baseURL}/node/?host=${author.host}`)
          .then((response) => {
            let node = createNodeObject(response, author.host);
            api
              .post(`${host}authors/${extractAuthorUUID(author.id)}/followers/${currentAuthor.uuid}`, { header: node.headers })
              .then((response) => {
                if (response.data) {
                  setIsFollowing(response.data);
                  setFollowState("following");
                } else {
                  setFollowState("notFollowing");
                }
              })
              .catch((error) => {
                console.log("Failed to get check if current author is following " + error);
              });
        });
      } else {
        await api
          .get(`${baseURL}/authors/${author_id}/followers/${currentAuthor.uuid}`)
          .then((response) => {
            if (response.data) {
              setIsFollowing(response.data);
              setFollowState("following");
            } else {
              setFollowState("notFollowing");
            }
          })
          .catch((error) => {
            console.log(
              "Failed to get check if current author is following " + error
            );
          });
      }
    };
    following();
  }, [isFollowing, useLocation().state]);

  const handleClick = () => {
    if (followState === "notFollowing") {
      host = baseURL + "/"
      setFollowState("followSent");
      if (postAuthorBaseApiURL != null) {
        host = postAuthorBaseApiURL
      }
      // Send a friend request object to the inbox of the author we're viewing
      api
        .post(`${host}authors/${author_id}/inbox/`, {
          type: "follow",
          summary: `${currentAuthor.displayName} wants to follow ${props.authorViewing.displayName}`,
          actor: currentAuthor,
          object: props.authorViewing,
        })
        .then((response) => {
          console.log("Success sending a friend request: " + response);
        })
        .catch((error) => {
          setFollowState("notFollowing");
      });
    } else if (followState === "following") {
      host = baseURL + "/"
      if (postAuthorBaseApiURL != null) {
        host = postAuthorBaseApiURL
      }
      // if we're already following, clicking will unfollow
      api
        .delete(
          `${host}authors/${author_id}/followers/${currentAuthor.uuid}`
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
