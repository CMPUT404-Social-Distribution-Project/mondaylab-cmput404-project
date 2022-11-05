import React, { useState, useContext, useEffect } from 'react';
import { Modal, Button, Form, CloseButton, Card, Container, ModalHeader } from "react-bootstrap";
import useAxios from '../../utils/useAxios';
import "./CreatePost.css";
import AuthContext from "../../context/AuthContext";
import { FaImage, FaLink } from "react-icons/fa";

export default function CreatePost(props) {
    const [show, setShow] = useState(true);
    const [showURI, setShowURI] = useState(false);
    const [unlist, setUnlist] = useState(false);
    const [isActive, setIsActive] = useState(false);
    const [eveActive, setEveActive] = useState(true);
    const [friActive, setFriActive] = useState(false);
    const [priActive, setPriActive] = useState(false);
    const { authTokens } = useContext(AuthContext);
    const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
    const api = useAxios();
    const user_id = localStorage.getItem("user_id");
    const [authorsArray, setAuthorsArray] = useState([])
    const [input, setInput] = useState('');
    const [filteredArray, setFilteredArray] = useState([])
    const [imagePost, setImagePost] = useState("");
    const [uri, setURI] = useState("");
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
    });

    /**
     * In order to change the color of the button when selecting a visibility option, whenever the user clicks on one of the options,
     * we set that as active (EveActive = Everyone, FriActive = Friends-only, PriActive = private) and set the other as false, these
     * variables are used in the style tag to determine if they are active (if so we change the text and background color of that button).
     *
     * @param {*} option
     */

    const setVisibility = (option) => {
        setPost({...post, visibility: option})
        setImagePost({...imagePost, visiblity: option})
        if(option === "PUBLIC"){
            setEveActive(true)
            setFriActive(false)
            setPriActive(false)
        } else if (option === "PRIVATE") {
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
        if (unlist) {
            setIsActive(true)
            setPost({ ...post, unlisted: true })
        } else {
            setIsActive(false)
            setPost({ ...post, unlisted: false })
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
        // No image
        if (imagePost === '') {
            api
            .post(`${baseURL}/authors/${user_id}/posts/`, post)
            .then((response) => {
                console.log(response.data);
                setShow(false)
                if (post.unlisted) {
                    setURI(response.data.id)
                    setShowURI(true)
                }
            })
            .catch((error) => {
                alert(`Something went wrong posting! \n Error: ${error}`)
                console.log(error);
            });
        } else {
            // there is an image, then we create an unlisted image post
            api
            .post(`${baseURL}/authors/${user_id}/posts/`, imagePost)
            .then((response) => {
                console.log(response.data);
                // image post created successfully, now link the post with the image post
            })
            .catch((error) => {
                alert(`Something went wrong posting! \n Error: ${error}`)
                console.log(error);
            });
        }

    };

    const searchAuthors = (value) => {
        setInput(value);
        if(input !== ''){
            const filteredData = authorsArray.filter((item) => {
                return Object.values(item.displayName).join('').toLowerCase().includes(input.toLowerCase());
            })
            setFilteredArray(filteredData);
        } else {
            setFilteredArray(authorsArray);
        }
    }

    function CheckInputLength () {
        console.log(authorsArray)
        if(authorsArray.length === 0){
            return (
                <Card>
                    <Card.Body>
                        No authors available
                    </Card.Body>
                </Card>
            )
        } else {
            if(input.length > 1 ) {
                    filteredArray.map((item) => {
                        return (
                            <Card>
                                <Card.Body>
                                    {item.profileImage}
                                    {item}
                                </Card.Body>
                            </Card>
                        )
                    })
            } else {
                authorsArray.map((item) => {
                    return (
                        <Card>
                            <Card.Body>
                                {item.profileImage}
                                {item.displayName}
                            </Card.Body>
                        </Card>
                    )
                })
            }
        }
    }

    const [file, setFile] = useState();
    const [imagePreview, setImagePreview] = useState('');
    const [base64, setBase64] = useState('');
    const [name, setFileName] = useState();
    const [size, setSize] = useState();
    const [isLoading, setIsLoading] = useState(false);

    const onImageChange = (e) => {
        console.log('file', e.target.files[0]);
        let file = e.target.files[0];
        if (file) {

            const reader = new FileReader();
            reader.onload = _handleReaderLoaded;
            reader.readAsBinaryString(file);
        }
    }
    
    const _handleReaderLoaded = (readerEvt) => {
        let binaryString = readerEvt.target.result;
        setBase64(btoa(binaryString));
    }
    
    const onFileSubmit = (e) => {
        setIsLoading(true);
        e.preventDefault();
        console.log('bine', base64);
        let payload = { image: base64 };
        console.log('payload', payload);

        setTimeout(() => {
            setIsLoading(false)
        }, 2000);
    }
    const imageUpload = (e) => {
        e.preventDefault();
        const reader = new FileReader();
        const file = e.target.files[0];
        console.log('reader', reader);
        console.log('file', file);
        if (reader !== undefined && file !== undefined) {
          reader.onloadend = () => {
            setFile(file);
            setSize(file.size);
            setFileName(file.name);
            setImagePreview(reader.result);
            setImagePost({
                title: "",
                source: "",
                description: "",
                contentType: file.type,
                content: reader.result,
                categories: "",
                visibility: "PUBLIC",
                unlisted: true,
            })
          }
          reader.readAsDataURL(file);
        };
    };

    const removeImage = () => {
        setFile('');
        setImagePreview('');
        setBase64('');
        setFileName('');
        setSize('');
        setImagePost('');
    };

    return (
        <>
            <div class="post-modal">
                <Modal size="lg"
                    show={show}
                    aria-labelledby="contained-modal-title-vcenter"
                    className="create-post-modal"
                    centered
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
                                        setVisibility("PUBLIC")
                                    }}>
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
                                <CloseButton className='me-2' variant="white" style={{ marginTop: "1%" }} onClick={props.onHide} />
                            </div>
                        </Modal.Header>
                        <Modal.Body>
                            <Form.Group className="title">
                                <Form.Control label="title" name="title" type="text" placeholder="Title"
                                    onChange={(e) => {
                                        setPost({
                                            ...post,
                                            title: e.target.value,
                                        })
                                    }} />
                            </Form.Group>
                            <Form.Group>
                                <Form.Control as="textarea" className="body" type="content" placeholder="Write you Post..."
                                    onChange={(e) => {
                                        setPost({
                                            ...post,
                                            content: e.target.value,
                                        })
                                    }} />
                                <Form.Control.Feedback type="invalid">
                                    Please choose a walk type.
                                </Form.Control.Feedback>
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
            </div>
            <div>
                <Modal
                    className="uri-modal"
                    show={showURI}
                    aria-labelledby="contained-modal-title-vcenter"
                    centered>
                    <Modal.Header>
                        <Modal.Title>
                            Unlisted Post Created!
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group>
                            <Form.Label style={{ color: "#BFEFE9", paddingBottom: "3%" }}>Shareable URI:</Form.Label>
                            <Form.Control readOnly size="lg" defaultValue={uri} />
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        
                        {imagePreview === '' ? <FaImage/> : <img src={imagePreview} alt="postImage"/>}
                        <form onSubmit={(e) => onFileSubmit(e)} onChange={(e) => onImageChange(e)} >
                            <input type="file" name="file" accept='.jpeg, .png, .jpg' onChange={imageUpload}/>
                        </form>
                        {imagePreview === '' ? <></> : <Button className="remove-image" onClick={removeImage}>Remove Image</Button>}
                        <FaLink className="link" onClick={(e) => {
                            setPost({
                                ...post,
                                contentType: "link",
                            });
                        }} />
                        <Button className="ok-button" size="lg" onClick={() => setShowURI(false)}> OK! </Button>
                    </Modal.Footer>
                </Modal>
            </div>
        </>
    );
}



