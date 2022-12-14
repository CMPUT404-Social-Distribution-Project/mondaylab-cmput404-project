import React from "react";
import Card from "react-bootstrap/Card";
import "./UserCard.css";
import { useNavigate } from "react-router-dom";
import { extractAuthorUUID } from "../utils/utils"

export default function UserCard(props) {
  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${extractAuthorUUID(props.author.id)}/`, { state: { refresh: true } });
  };

  return (
    <Card onClick={routeChange} className="userCard">
      <Card.Body>
        <Card.Title>
          <div className="profilePicCard">
            <img
              id="profilePicCard"
              src={props.author.profileImage}
              alt="profilePic"
            />
          </div>
          <div className="text">{props.author.displayName}</div>
        </Card.Title>
      </Card.Body>
    </Card>
  );
}
