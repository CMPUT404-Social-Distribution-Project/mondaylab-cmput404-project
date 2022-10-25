import React from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import "./PostCard.css"

export default function PostCard(props) {
  return (
    <Card style={{ width: '30rem'}}>
      <Card.Header>
        <div className="profilePicPage">
          <img id="profilePicPage" src={props.post.author.profileImage} alt="profilePic"/>
        </div>
      </Card.Header>
      <Card.Img variant="top" src="" />
      <Card.Body>
        <Card.Title>{props.post.title}</Card.Title>
        <Card.Text>
          {props.post.content}
        </Card.Text>
        <hr/>
        <div className="comments-container">
          <div className="comments-text">
              Comments
          </div>
          <div className="comments">
              {/* show max 5 comments, have option to show more */}
          </div>
        </div>

      </Card.Body>
    </Card>
  );
}
