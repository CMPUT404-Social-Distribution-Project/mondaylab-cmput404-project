import React, { useContext } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import "./FollowRequestCard.css";
import { useNavigate } from "react-router-dom";
import useAxios from "../../utils/useAxios";
import AuthContext from "../../context/AuthContext";

export default function FollowRequestCard(props) {
    // pass in the follow request object in props
    const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
    const user_id = localStorage.getItem("user_id");  // the currently logged in author
    const api = useAxios();

    const navigate = useNavigate();
    const routeChange = () => {
        navigate(`/authors/${props.followRequest.actor.uuid}/`);
    }

    const handleAccept = async () => {
        await api      
        .put(`${baseURL}/authors/${user_id}/followers/${props.followRequest.actor.uuid}`)
        .then((response) => {
            console.log(`Success adding ${props.followRequest.actor.displayName} to followers` + response.data);
            window.location.reload();
        })
        .catch((error) => {
            console.log("Failed to add to followers. " + error);
        });
    };

    const handleDecline = async () => {
        await api      
        .delete(`${baseURL}/authors/${user_id}/inbox/${props.followRequest.actor.uuid}`)
        .then((response) => {
            console.log("Success deleting request " + response.data);
            window.location.reload();
        })
        .catch((error) => {
            console.log("Failed to delete request. " + error);
        });
        
    }

  return (
    <Card className="follow-request-card">
      <Card.Header
        onClick={routeChange}
        >
        <Card.Title>
            <div className="profilePicCard">
            <img id="profilePicCard" src={props.followRequest.actor.profileImage} alt="profilePic"/>
            </div>
            <div className="text">{props.followRequest.actor.displayName}</div>
        </Card.Title>
      </Card.Header>
      <Card.Body>
        <Button className="accept-button" onClick={handleAccept}>Accept</Button>
        <Button className="decline-button" onClick={handleDecline}>Decline</Button>
      </Card.Body>
    </Card>
  );
}
