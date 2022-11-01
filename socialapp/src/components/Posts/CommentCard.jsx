import React from 'react';
import { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import "./PostCard.css";

export default function CommentCard(props) {
    return (
        <Card>
            <Card.Body style={{ width: "auto", display: "flex"}}>
                <div className="profile-pic-post">
                    <img src={props.author.profileImage} alt="profilePic" />
                </div>
                <div style={{marginTop: "2%",marginLeft: "5%"}}>
                    {props.comment}
                </div>
            </Card.Body>
        </Card>
    )
}