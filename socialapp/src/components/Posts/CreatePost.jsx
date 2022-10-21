import React, { useState } from 'react';
import { Modal, Button, InputGroup, Form, CloseButton } from "react-bootstrap";
import { SassColor } from 'sass';
import "./CreatePost.css";
import { FaImage, FaLink } from "react-icons/fa";

export default function Example() {
    const [show, setShow] = useState(true);
    const [post, setPost] = useState({
        title: "",
        source: "",
        orgin: "",
        description: "",
        contentType: "",
        content: "",
        author: "",
        categories: "",
        visibility: "",
        unlisted: "",
    })

    const closePost = () => {
        setShow(false)
    }

    return (
        <div class="post-modal">
            <Modal size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
                show={show}
                onHide={closePost}>
                <Modal.Header>
                    <Modal.Title className='header'>Make a Post | </Modal.Title>
                    <Modal.Title className="header1">Who can see this post?</Modal.Title>
                    <InputGroup>
                        <Button value="Everyone" className='option'name="view" />Everyone
                        <Button value="Friends" className='option' name="view"/>Friends-Only
                        <Button value="Private" className='option' name="view" />Private
                    </InputGroup>
                    <Button className="unlist"> Unlisted </Button>
                    <CloseButton variant="white" onClick={closePost} />
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <InputGroup className="title">
                            <Form.Control type="title" placeholder="Title" />
                        </InputGroup>

                        <InputGroup>
                            <Form.Control className="body" type="content" placeholder="Write you Post..." />
                        </InputGroup>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <FaImage className="image" />
                    <FaLink className="link" />
                    <Button class="postButton" onClick={closePost}>
                        Post
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}
