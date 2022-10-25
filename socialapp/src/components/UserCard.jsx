import React from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import "./UserCard.css"

export default function UserCard(props) {
  return (
    <Card>
      <Card.Body>
        <Card.Title>
            <div className="profilePicCard">
            <img id="profilePicCard" src={props.post.author.profileImage} alt="profilePic"/>
            </div>
            {props.author.displayName}
        </Card.Title>
      </Card.Body>
    </Card>
  );
}
