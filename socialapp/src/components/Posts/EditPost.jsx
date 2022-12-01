import React, { useState, useContext } from "react";
import {
  Modal,
  Button,
  Form,
  CloseButton,
  Card
} from "react-bootstrap";
import useAxios from "../../utils/useAxios";
import "./CreatePost.css";
import AuthContext from "../../context/AuthContext";
import { FaImage, FaLink, FaSearch } from "react-icons/fa";
import { search2 } from "../../utils/searchUtil";
import UserCard from "../UserCard.jsx";
import { extractAuthorUUID } from "../../utils/utils";

export default function EditPost(props) {
  const [showURI, setShowURI] = useState(false);
  const [unlist, setUnlist] = useState(() =>
    props.post.unlisted ? true : false
  );
  const [eveActive, setEveActive] = useState(() =>
    props.post.visibility === "PUBLIC" ? true : false
  );
  const [friActive, setFriActive] = useState(() =>
    props.post.visibility === "FRIENDS" ? true : false
  );
  const [priActive, setPriActive] = useState(() =>
    props.post.visibility === "PRIVATE" ? true : false
  );
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const api = useAxios();
  const user_id = localStorage.getItem("user_id");
  const [imagePost, setImagePost] = useState(null);
  const [uri, setURI] = useState("");
  const propsPost = props.post;
  delete propsPost.commentSrc; // causing issue with updating.
  const [post, setPost] = useState(propsPost);
  const [showLinkForm, setShowLinkForm] = useState(() =>
    props.post.image ? true : false
  );
  const [sendTo, setSendTo] = useState(null);
  const [selectedAuthor, setSelectedAuthor] = useState(null);
  const [loading, setLoading] = useState(false);
  const [authors, setAuthors] = useState(null);
  const [value, setValue] = useState("");


  /**
   * In order to change the color of the button when selecting a visibility option, whenever the user clicks on one of the options,
   * we set that as active (EveActive = Everyone, FriActive = Friends-only, PriActive = private) and set the other as false, these
   * variables are used in the style tag to determine if they are active (if so we change the text and background color of that button).
   *
   * @param {*} option
   */

  const setVisibility = (option) => {
    setPost({ ...post, visibility: option });
    if (imagePost) {
      setImagePost({ ...imagePost, visiblity: option });
    }
    if (option === "PUBLIC") {
      setEveActive(true);
      setFriActive(false);
      setPriActive(false);
    } else if (option === "PRIVATE") {
      setEveActive(false);
      setFriActive(false);
      setPriActive(true);
    } else {
      setEveActive(false);
      setFriActive(true);
      setPriActive(false);
    }
  };

  /**
   * Once the user clicks the unlisted button, we set unlisted to the opposite of the current variable value.
   * This way, if the user had previously clicked unlisted before, this changes it to false and viceversa. So
   * we set unlisted to the correct value depending on is unlist is true or not.
   *
   */

  const unlistPost = () => {
    if (unlist) {
      setUnlist(false);
      setPost({ ...post, unlisted: false });
    } else {
      setUnlist(true);
      setPost({ ...post, unlisted: true });
    }
  };

  /**
   * When the users click the button "Post", we will use the information created in the variable post to send it to the API.
   * We use the user_id (created using useCOntext of the current autheticated user) to create a path to posts, and we autheticated
   * it using our auth token. If the request is successful we send a response to the console and call the function closePost. If not
   * we will send the error to the console and the error will not be logged.
   *
   */

   const sendPost = async (response) => {
    if (post.unlisted) {
      setURI(
        `${window.location.protocol}//${window.location.host}/authors/${user_id}/posts/${response.data.uuid}`
      );
      setShowURI(true);
      props.onHide();
    } else {
      if (post.visibility === "PRIVATE") {
        if (sendTo === null) {
          alert("Select an author to send to!");
          return;
        }
        const resultPost = response.data;
        api
          .post(`${baseURL}/authors/${extractAuthorUUID(sendTo.id)}/inbox/`, resultPost)
          .then((response) => {
            console.log(`Success sending private post to inbox of ${sendTo.displayName}`);
          })
          .catch((error) => {
            console.log("Failed to send private post. " + error);
          });
      }
      props.onHide();
    }
  }

  const handleSubmitPost = async () => {
    // No image
    if (!imagePost) {
        await api
          .post(`${baseURL}/authors/${user_id}/posts/${props.post.uuid}`, post)
          .then((response) => {
            sendPost(response);
            })
          .catch((error) => {
            alert(`Something went wrong posting! \n Error: ${error.response.data}`);
            console.log(error);
          });
    } else {
        // there is an image, then we create an unlisted image post
        await api
          .post(`${baseURL}/authors/${user_id}/posts/`, imagePost)
          .then((response) => {
            // image post created successfully, now link the post with the image post
            // set the image field
            const new_post = {
              ...post,
              image: `${baseURL}/authors/${user_id}/posts/${response.data.uuid}/image`,
            };
            return api.post(`${baseURL}/authors/${user_id}/posts/${props.post.uuid}`, new_post);
          })
          .then((response) => {
            sendPost(response);
          })
          .catch((error) => {
            alert(
              `Something went wrong posting the image post! \n Error: ${error.response.data}`
            );
            console.log(error.response);
          });
      }
  };

  // check if the post is the same; if so don't send.
  const postIsSame = () => {
    if (propsPost === post) {
      props.onHide();
    } else {
      handleSubmitPost();
    }
  };

  const [file, setFile] = useState();
  console.log("Editpost", props.post.image)
  const [imagePreview, setImagePreview] = useState(() => props.post.image === null ? "" : props.post.image);
  const [base64, setBase64] = useState("");
  const [name, setFileName] = useState();
  const [size, setSize] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const onImageChange = (e) => {
    let file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = _handleReaderLoaded;
      reader.readAsBinaryString(file);
    }
  };

  const _handleReaderLoaded = (readerEvt) => {
    let binaryString = readerEvt.target.result;
    setBase64(btoa(binaryString));
  };

  const onFileSubmit = (e) => {
    setIsLoading(true);
    e.preventDefault();
    let payload = { image: base64 };

    setTimeout(() => {
      setIsLoading(false);
    }, 2000);
  };
  const imageUpload = (e) => {
    e.preventDefault();
    const reader = new FileReader();
    const file = e.target.files[0];
    if (reader !== undefined && file !== undefined) {
      reader.onloadend = () => {
        setShowLinkForm(false);
        setFile(file);
        setSize(file.size);
        setFileName(file.name);
        setImagePreview(reader.result);
        setImagePost({
          title: "",
          source: "",
          description: "",
          contentType: file.type + ";base64",
          content: reader.result,
          categories: "",
          visibility: "PUBLIC",
          unlisted: true,
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setFile("");
    setImagePreview("");
    setBase64("");
    setFileName("");
    setSize("");
    setImagePost(null);
    setPost({ ...post, image: "" });
  };

  const hiddenFileInput = React.useRef(null);
  const handleImageClick = () => {
    hiddenFileInput.current.click();
  };

  const linkClickHandler = () => {
    setShowLinkForm(!showLinkForm);
    setImagePreview("");
    delete post.image;
    setPost(post);
    setImagePost(null);
  }

  const search = async (val) => {
    setLoading(true);
    const res = await search2(
      `${baseURL}/authors?search=${val}&size=3`
    );
    setAuthors(res);

    setLoading(false);
  };

  const onChangeHandler = async (e) => {
    search(e.target.value);
    setValue(e.target.value);
  };

  const privatePost = (author) => {
    setSendTo(author);
    setValue(author);
    setSelectedAuthor(author);
    setAuthors();
  }

  function RenderAuthors(props) {
    // given the list of authors from the query, creates the user cards
    if (props.authors) {
      return (
        <div className="private-search-authors">
          { props.authors.items !== "undefined" ? (
            props.authors.items.length !== 0 ? (
              props.authors.items.map((author) =>
                <div>
                  <Card onClick={() => {privatePost(author)}} className="userCard">
                    <Card.Body>
                      <Card.Title>
                        <div className="profilePicCard">
                          <img
                            id="profilePicCard"
                            src={author.profileImage}
                            alt="profilePic"
                          />
                        </div>
                        <div className="text">{author.displayName}</div>
                      </Card.Title>
                    </Card.Body>
                  </Card>
                </div>)
            ) : (
              <Card style={{ backgroundColor: "var(--darker-blue)", width: "50%", paddingTop: "1%" }}>
                <h5 className="no-author">
                  No match result for authors!
                </h5>
              </Card>
            )
          ) : null}
        </div>
      );
    }
    return <></>;
  }

  return (
    <>
      <div className="post-modal">
        <Modal
          size="lg"
          show={props.show}
          onHide={props.onHide}
          aria-labelledby="contained-modal-title-vcenter"
          className="create-post-modal"
          centered
        >
          <Form>
            <Modal.Header>
              <div
                style={{
                  margin: "0",
                  padding: "0",
                  width: "100%",
                  display: "flex",
                }}
              >
                <Modal.Title className="header">Edit Post | </Modal.Title>
                <Modal.Title className="header1">
                  Who can see this post?
                </Modal.Title>
                <Button
                  type="button"
                  value="Everyone"
                  className="option"
                  name="view"
                  style={{
                    backgroundColor: eveActive ? "var(--teal)" : "",
                    color: eveActive ? "var(--dark-blue)" : "",
                  }}
                  onClick={() => {
                    setVisibility("PUBLIC");
                  }}
                >
                  Everyone
                </Button>
                <Button
                  type="button"
                  value="Friends"
                  className="option"
                  name="view"
                  style={{
                    backgroundColor: friActive ? "var(--teal)" : "",
                    color: friActive ? "var(--dark-blue)" : "",
                  }}
                  onClick={() => {
                    setVisibility("FRIENDS");
                  }}
                >
                  Friends-Only
                </Button>
                <Button
                  type="button"
                  value="Private"
                  className="option"
                  name="view"
                  style={{
                    backgroundColor: priActive ? "var(--teal)" : "",
                    color: priActive ? "var(--dark-blue)" : "",
                  }}
                  onClick={() => {
                    setVisibility("PRIVATE");
                  }}
                >
                  Private
                </Button>
                <Button
                  style={{
                    backgroundColor: unlist ? "var(--teal)" : "",
                    color: unlist ? "var(--dark-blue)" : "",
                  }}
                  className="unlist"
                  onClick={unlistPost}
                >
                  Unlisted
                </Button>
                <CloseButton
                  className="me-2"
                  variant="white"
                  style={{ marginTop: "1%" }}
                  onClick={props.onHide}
                />
              </div>
            </Modal.Header>
            {(() => {
                  if (post.visibility === "PRIVATE") {
                    return (
                      <div className="private-search-container">
                        <FaSearch style={{
                        color: "#BFEFE9",
                        height: "1em",
                        width: "1em",
                        margin: "0.5em",
                        zIndex: "3px", }} className="FaSearch" />
                        <input
                          className="private-search-input"
                          value={value.displayName}
                          onChange={(e) => onChangeHandler(e)}
                          placeholder="Search for an author"
                        />
                        {value !== "" ? <RenderAuthors authors={authors} /> : null}
                        {selectedAuthor && <UserCard author={selectedAuthor} />}
                      </div>
                    )
                  }
                })()}
            <Modal.Body>
              <Form.Group className="title">
                <Form.Control
                  label="title"
                  name="title"
                  type="text"
                  placeholder="Title"
                  value={post.title}
                  onChange={(e) => {
                    setPost({
                      ...post,
                      title: e.target.value,
                    });
                  }}
                />
              </Form.Group>
              <Form.Group>
                <Form.Control
                  as="textarea"
                  className="body"
                  type="content"
                  placeholder="Write your Post..."
                  value={post.content}
                  onChange={(e) => {
                    setPost({
                      ...post,
                      content: e.target.value,
                    });
                  }}
                />
              </Form.Group>
              {showLinkForm && <Form.Group className="link-form">
                <Form.Control
                  label="link"
                  name="link"
                  type="text"
                  placeholder="Image URL link"
                  value={post.image}
                  onChange={(e) => {
                    setPost({
                      ...post,
                      image: e.target.value,
                    });
                    setImagePreview(e.target.value);
                  }}
                />
              </Form.Group>}
            </Modal.Body>
            {imagePreview === "" ? (
              <></>
            ) : (
              <img
                className="image-preview"
                src={imagePreview}
                alt="postImage"
              />
            )}
            <Modal.Footer>
              <div className="image-upload-container">
                <FaImage className="image-upload" onClick={handleImageClick} />
                <form
                  onSubmit={(e) => onFileSubmit(e)}
                  onChange={(e) => onImageChange(e)}
                >
                  <input
                    type="file"
                    name="file"
                    accept=".jpeg, .png, .jpg"
                    onChange={imageUpload}
                    ref={hiddenFileInput}
                    style={{ display: "none" }}
                  />
                </form>
                {imagePost ? (
                  <Button className="remove-image" onClick={removeImage}>
                    Remove Image
                  </Button>
                ) : (
                  <></>
                )}
                <FaLink className="link-icon" onClick={() => linkClickHandler()}/>
              </div>
              <Button className="postButton" onClick={postIsSame}>
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
          centered
        >
          <Modal.Header>
            <Modal.Title>Unlisted Post Created!</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group>
              <Form.Label style={{ color: "var(--teal)", paddingBottom: "3%" }}>
                Shareable URI:
              </Form.Label>
              <Form.Control readOnly size="lg" defaultValue={uri} />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button
              className="ok-button"
              size="lg"
              onClick={() => {
                setShowURI(false);
                props.onHide();
              }}
            >
              
              OK!
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    </>
  );
}
