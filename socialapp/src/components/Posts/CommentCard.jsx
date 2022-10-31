import React from 'react';
import { Card } from 'react-bootstrap';

export default function CommentCard(props){
    return (
        <Card>
            <Card.Body style={{width: "auto"}}>
                {props.comment}
            </Card.Body>
        </Card>
    )
}