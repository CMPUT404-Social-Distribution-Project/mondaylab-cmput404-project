import React, { useEffect, useState, useContext } from 'react';
import Button from 'react-bootstrap/Button';
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import useAxios from '../utils/useAxios';


export default function FollowButton(props) {
  const [res, setRes] = useState("");
  // if not the current user, make the button visible
  const [isNotCurrentUser, setIsNotCurrentUser] = useState(true);
  const api = useAxios();                             // use this to add authorization header
  const user_id = localStorage.getItem("user_id");    // current user

  const [followSent, setFollowSent] = useState(false);

  useEffect(() => {
    if (user_id === props.id) {
      // if the current user (user_id) has the same id in the url, don't show follow button
      setIsNotCurrentUser(false)
    }
  })

  const handleClick = () => {
    setFollowSent(true)
    // Add the current author to the followers list of the author that current is viewing
    api.put(`http://127.0.0.1:8000/service/authors/${props.id}/followers/${user_id}`, {})
    .then((response) => {
      console.log("Success sending a friend request: " + response);
    })
    .catch((error) => {
      console.log("Failed to follow: "+error);
      setFollowSent(false)
    });
  };

  return (
    <Button
      id="followButton"
      variant="primary"
      disabled={followSent}
      onClick={!followSent ? handleClick : null}
      style={{visibility: isNotCurrentUser ? 'visible' : 'hidden'}}
    >
      {followSent ? 'Sent' : 'Follow'}
    </Button>
  );
}
