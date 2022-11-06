import React from "react";
import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";
import "./CommentCard.css";
import { useNavigate } from "react-router-dom";

export default function CommentCard(props) {
  const navigate = useNavigate();
  const routeChange = () => {
    navigate(`/authors/${props.author.uuid}/`, { state: { refresh: true } });
  };

  return (
    <Card className="comment-card">
      <Card.Body style={{ width: "auto", display: "flex" }}>
        <div className="comment-author-container" onClick={routeChange}>
          <div className="comment-profile-pic">
            <img src={props.author.profileImage} alt="profilePic" />
          </div>
          <div className="comment-author">{props.author.displayName}</div>
        </div>
        <div className="comment-content">{props.comment}</div>
      </Card.Body>
    </Card>
  );
}
