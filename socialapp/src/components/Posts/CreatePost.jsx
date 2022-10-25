import React, { useState, useContext } from 'react';
import { Modal, Button, InputGroup, Form, CloseButton } from "react-bootstrap";
import axios from 'axios';
import "./CreatePost.css";
import AuthContext from "../../context/AuthContext";
import { FaImage, FaLink } from "react-icons/fa";

export default function Example() {
    const [show, setShow] = useState(true);
    const [unlist, setUnlist] = useState(false)
    const [isActive, setIsActive] = useState(false)
    const [eveActive, setEveActive] = useState(true)
    const [friActive, setFriActive] = useState(false)
    const [priActive, setPriActive] = useState(false)
    const { authTokens } = useContext(AuthContext);
    const user_id = localStorage.getItem("user_id");
    const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
    const [post, setPost] = useState({
        title: "",
        source: "",
        orgin: "",
        description: "",
        contentType: "text/plain",
        content: "",
        categories: "",
        visibility: "PUBLIC",
        unlisted: false,
    })

    /**
     * In order to change the color of the button when selecting a visibility option, whenever the user clicks on one of the options,
     * we set that as active (EveActive = Everyone, FriActive = Friends-only, PriActive = private) and set the other as false, these
     * variables are used in the style tag to determine if they are active (if so we change the text and background color of that button).
     * 
     * @param {*} option 
     */

    const setVisibility = (option) => {
        setPost({...post, visibility: option})
        if(option === "PUBLIC"){
            setEveActive(true)
            setFriActive(false)
            setPriActive(false)
        } else if(option === "PRIVATE"){
            setEveActive(false)
            setFriActive(true)
            setPriActive(false)
        } else {
            setEveActive(false)
            setFriActive(false)
            setPriActive(true)
        }
    }

    const unlistPost = () => {
        setUnlist(!unlist)
        if(unlist){
            setIsActive(true)
            setPost({...post, unlisted: true})
        } else {
            setIsActive(false)
            setPost({ ...post, unlisted: false})
        }
    };

    /**
     * When the users click the button "Post", we will use the information created in the variable post to send it to the API.
     * We use the user_id (created using useCOntext of the current autheticated user) to create a path to posts, and we autheticated
     * it using our auth token. If the request is successful we send a response to the console and call the function closePost. If not
     * we will send the error to the console and the error will not be logged. 
     * 
     */

    const sendPost = () => {
        axios
            .post(`${baseURL}/authors/${user_id}/posts/`, post, 
            { headers: { 'Authorization': `Bearer ${authTokens.access}` }})
            .then((response) => {
                console.log(response.data);
                closePost();
            })
            .catch((error) => {
                alert(`Something went wrong posting! \n Error: ${error}`)
                console.log(error);
            });
    };

    /**
     * If the user clicks on the x button at the top corner of the post (or if they send a valid post), then the function
     * will set show to false (show is what is used by the Modal to determine if it should stay up or not).
     * 
     */

    const closePost = () => {
        setShow(false)
    };

    return (
        /**
         * The modal is comprised of different buttons and input groups that are used to fill in the post variable (this variable as a dictionary,
         * is then sent to the api). Each time a user presses a button or types in a field, that corresponding dictionary value is filled/updated. 
         * 
         */

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
                        <Button type="radio" value="Everyone" className='option' name="view" 
                            style={{
                                backgroundColor: eveActive ? ' #BFEFE9' : '',
                                color: eveActive ? 'black' : '',
                            }} 
                            onClick={() => {
                                setVisibility("PUBLIC")}}>
                        Everyone </Button>
                        <Button type="radio" value="Friends" className='option' name="view" 
                            style={{
                                backgroundColor: friActive ? ' #BFEFE9' : '',
                                color: friActive ? 'black' : '',
                            }} 
                            onClick={() => {
                                setVisibility("FRIENDS")
                            }}>
                        Friends-Only </Button>
                        <Button type="radio" value="Private" className='option' name="view" 
                            style={{
                                backgroundColor: priActive ? ' #BFEFE9' : '',
                                color: priActive ? 'black' : '',
                            }} 
                            onClick={() => {
                                setVisibility("Private")
                            }}>
                        Private </Button>
                    </InputGroup>
                    <Button style={{
                        backgroundColor: isActive ? ' #BFEFE9' : '',
                        color: isActive ? 'black' : '',
                    }} className="unlist" onClick={unlistPost}> 
                    Unlisted 
                    </Button>
                    <CloseButton className='me-2' variant="white" onClick={closePost} />
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <InputGroup className="title">
                            <Form.Control required type="title" placeholder="Title" 
                                onChange={(e) => {
                                    setPost({
                                        ...post,
                                        title: e.target.value,
                                    })}} />
                        </InputGroup>
                        <InputGroup>
                            <Form.Control required className="body" type="content" placeholder="Write you Post..."
                                onChange={(e) => {
                                    setPost({
                                        ...post,
                                        content: e.target.value,
                                    })
                                }} />
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
