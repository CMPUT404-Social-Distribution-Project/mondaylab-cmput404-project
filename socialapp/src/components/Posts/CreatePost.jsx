import React, { useState } from 'react';
import { Modal, Button, InputGroup, Form, CloseButton } from "react-bootstrap";
import { SassColor } from 'sass';
import "./CreatePost.css";
import { FaImage, FaLink } from "react-icons/fa";

export default function Example() {
    const [show, setShow] = useState(true);
    const [unlist, setUnlist] = useState(false);
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

    const unlisted = () => {
    }


    const sendPost = () => {

    }

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
                        <Button type="radio" value="Everyone" className='option' name="view" onClick={(e) => {
                            setPost({
                                ...post,
                                visibility: "Everyone",
                            });
                        }}>Everyone </Button>
                        <Button type="radio" value="Friends" className='option' name="view" onClick={(e) => {
                            setPost({
                                ...post,
                                visibility: "Friends",
                            });
                            }}>Friends-Only </Button>
                        <Button type="radio" value="Private" className='option' name="view" onClick={(e) => {
                            setPost({
                                ...post,
                                visibility: "Private",
                            });
                            }}>Private </Button>
                    </InputGroup>
                    <Button className="unlist" onClick={unlisted()}> Unlisted </Button>
                    <CloseButton className='me-2' variant="white" onClick={closePost} />
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <InputGroup className="title">
                            <Form.Control type="title" placeholder="Title"/>
                        </InputGroup>
                        <InputGroup>
                            <Form.Control className="body" type="content" placeholder="Write you Post..."/>
                        </InputGroup>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <FaImage className="image" onClick={(e) => {
                        setPost({
                            ...post,
                            contentType: "image",
                        });
                    }} />
                    <FaLink className="link" onClick={(e) => {
                        setPost({
                            ...post,
                            contentType: "link",
                        });
                    }} />
                    <Button className="postButton" onClick={sendPost}>
                        Post
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}
