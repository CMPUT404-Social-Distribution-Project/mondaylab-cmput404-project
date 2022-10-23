import React, { useEffect, useState, useContext } from 'react';
import Button from 'react-bootstrap/Button';
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import useAxios from '../utils/useAxios';

function simulateNetworkRequest() {

}

export default function FollowButton(props) {
  const [res, setRes] = useState("");
  // if not the current user, make the button visible
  const [isNotCurrentUser, setIsNotCurrentUser] = useState(true);

  const api = useAxios();
  const user_id = localStorage.getItem("user_id");    // current user

  const [followSent, setFollowSent] = useState(false);
  console.log("The author id passed into follow button is: " + props.id)

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
      console.log("The response was: " + response);
    })
    .catch((error) => {
      console.log(error);
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
