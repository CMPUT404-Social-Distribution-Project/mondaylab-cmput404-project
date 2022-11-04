import React, { useState, useContext} from 'react';
import { Modal, Button, Form, CloseButton, Card} from "react-bootstrap";
import useAxios from '../../utils/useAxios';
import "./CreatePost.css";
import AuthContext from "../../context/AuthContext";
import { FaImage, FaLink } from "react-icons/fa";
import { search2 } from "../../utils/searchUtil";
import { FaSearch } from "react-icons/fa";

function RenderAuthors(props) {
    // given the list of authors from the query, creates the user cards
    console.log(props.authors)
    if (props.authors) {
        return (
            <div className="authors-explore-container">
                {
                    typeof props.authors.items !== 'undefined' ? props.authors.items.map((author) => 
                        <Card
                            className="userCard"
                        >
                            <Card.Body onClick={console.log("hello")}>
                                <Card.Title>
                                    <div className="profilePicCard">
                                        <img id="profilePicCard" src={author.profileImage} alt="profilePic" />
                                    </div>
                                    <div className="text">{author.displayName}</div>
                                </Card.Title>
                            </Card.Body>
                        </Card>) 
                    : null
                }
            </div>
        )
    }
    return <></>;
}

export default function CreatePost(props) {
    const [showModal, setShowModal] = useState(true)
    const [showURI, setShowURI] = useState(false)
    const [unlist, setUnlist] = useState(false)
    const [isActive, setIsActive] = useState(false)
    const [eveActive, setEveActive] = useState(true)
    const [friActive, setFriActive] = useState(false)
    const [priActive, setPriActive] = useState(false)
    const { authTokens } = useContext(AuthContext);
    const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
    const api = useAxios();
    const user_id = localStorage.getItem("user_id");
    const [authors, setAuthors] = useState([])
    const [value, setValue] = useState('');
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
            setFriActive(false)
            setPriActive(true)
        } else {
            setEveActive(false)
            setFriActive(true)
            setPriActive(false)
        }
    }

    /**
     * Once the user clicks the unlisted button, we set unlisted to the opposite of the current variable value.
     * This way, if the user had previously clicked unlisted before, this changes it to false and viceversa. So
     * we set unlisted to the correct value depending on is unlist is true or not.
     * 
     */

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
        api
            .post(`${baseURL}/authors/${user_id}/posts/`, post)
            .then((response) => {
                props.onHide()
                if (post.unlisted){
                    setShowURI(true)
                }
            })
            .catch((error) => {
                alert(`Something went wrong posting! \n Error: ${error}`)
                console.log(error);
            });
    };

    const search = async val => {
        const res = await search2(
            `${baseURL}/authors?search=${val}`      // TODO: need to search with pagination
        );
        console.log(res);
        setAuthors(res);
    };

    const onChangeHandler = async e => {
        search(e.target.value);
        setValue(e.target.value);
    }

    return (
        <div class="post-modal">
            <Modal size="lg"
                {...props}
                aria-labelledby="contained-modal-title-vcenter"
                className="create-post-modal"
                centered
                show={showModal}
            >
                <Form>
                    <Modal.Header >
                        <div style={{ margin: "0", padding: "0", width: "100%", display: "flex" }}>
                            <Modal.Title className='header'>Make a Post | </Modal.Title>
                            <Modal.Title className="header1">Who can see this post?</Modal.Title>
                            <Button type="button" value="Everyone" className='option' name="view" 
                                style={{
                                    backgroundColor: eveActive ? ' #BFEFE9' : '',
                                    color: eveActive ? 'black' : '',
                                }} 
                                onClick={() => {
                                    setVisibility("PUBLIC")}}>
                            Everyone </Button>
                            <Button type="button" value="Friends" className='option' name="view" 
                                style={{
                                    backgroundColor: friActive ? ' #BFEFE9' : '',
                                    color: friActive ? 'black' : '',
                                }} 
                                onClick={() => {
                                    setVisibility("FRIENDS")
                                }}>
                            Friends-Only </Button>
                            <Button type="button" value="Private" className='option' name="view" 
                                style={{
                                    backgroundColor: priActive ? ' #BFEFE9' : '',
                                    color: priActive ? 'black' : '',
                                }} 
                                onClick={() => {
                                    setVisibility("PRIVATE")
                            }}>
                                Private 
                            </Button>
                            <Button style={{
                                backgroundColor: isActive ? ' #BFEFE9' : '',
                                color: isActive ? 'black' : '',
                                }} className="unlist" onClick={unlistPost}> 
                                Unlisted 
                            </Button>
                            <CloseButton className='me-2' variant="white" style={{ marginTop: "1%"}}onClick={props.onHide} />
                        </div>
                    </Modal.Header>
                    <Modal.Header id="modal-header">
                        {
                            priActive
                                ? <div>
                                        <FaSearch className="FaSearch"/>
                                        <input
                                            className="search-bar-author"
                                            value={value}
                                            onChange={e => onChangeHandler(e)}
                                            placeholder="Search for an author"
                                        />
                                    <RenderAuthors authors={authors}/>
                                 </div>
                                : ""
                        }   
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group className="title">
                            <Form.Control label="title" name="title" type="text" placeholder="Title" 
                                onChange={(e) => {
                                    setPost({
                                        ...post,
                                        title: e.target.value,
                                    })}} />
                        </Form.Group>
                        <Form.Group>
                            <Form.Control as="textarea" className="body" type="content" placeholder="Write you Post..."
                                onChange={(e) => {
                                    setPost({
                                        ...post,
                                        content: e.target.value,
                                    })
                            }} />
                        </Form.Group>
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
                </Form>
            </Modal>
            <Modal 
                aria-labelledby="contained-modal-title-vcenter"
                className="create-post-modal"
                centered
                show={showURI}>
                    Hello
            </Modal>
        </div>
    );
}
