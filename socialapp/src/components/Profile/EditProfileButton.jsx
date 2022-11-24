import React, { useContext } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import { Formik, Form } from "formik";
import TextField from "../TextField";
import * as Yup from "yup";
import useAxios from "../../utils/useAxios.js";
import AuthContext from "../../context/AuthContext";
import "./EditProfileButton.css";

function VerticallyCenteredModal(props) {
  const validate = Yup.object().shape({
    profileImage: Yup.string().url(),
    username: Yup.string().required("Required").max(128, "Invalid username"),
    github: Yup.string().url(),
  });

  const api = useAxios();
  const { baseURL } = useContext(AuthContext);

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      contentClassName="edit-profile-modal"
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Edit Profile
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Formik
          initialValues={{
            profileImage: `${props.author.profileImage}`,
            username: `${props.author.displayName}`,
            github: `${props.author.github}`,
          }}
          validationSchema={validate}
          onSubmit={(values) => {
            const username = values.username;
            const profileImage = values.profileImage;
            const github = values.github;

            // If fields are the same as before, don't send
            const toSend = {
              displayName: `${username}`,
              ...(profileImage === props.author.profileImage
                ? {}
                : { profileImage: `${profileImage}` }),
              ...(github === props.author.github
                ? {}
                : { github: `${github}` }),
            };

            api
              .post(`${baseURL}/authors/${props.author.uuid}/`, toSend)
              .then((response) => {
                if (response.status === 202) {
                  localStorage.setItem("loggedInUser", response.data.user);
                  props.onHide();
                  window.location.reload(); // refreshes page...not ideal.
                }
              })
              .catch((err) => {
                if (err.response) {
                  alert("Failed to submit changes. " + err.response.data);
                }
              });
          }}
        >
          {(formik) => (
            <Form>
              <div>
                <TextField
                  label="Profile Image URL"
                  name="profileImage"
                  type="text"
                />
                <TextField label="Username" name="username" type="text" />
                <TextField label="GitHub" name="github" type="text" />
                <button
                  id="submit-button"
                  type="submit"
                  className="btn btn-primary"
                >
                  Submit
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </Modal.Body>
      <Modal.Footer>
        <button
          id="cancel-button"
          onClick={props.onHide}
          className="btn btn-primary"
        >
          Cancel
        </button>
      </Modal.Footer>
    </Modal>
  );
}

export default function EditProfileButton(props) {
  const [modalShow, setModalShow] = React.useState(false);
  const user_id = localStorage.getItem("user_id");

  if (user_id === props.author.uuid) {
    return (
      <div className="edit-profile">
        <Button
          className="edit-profile-button"
          variant="primary"
          onClick={() => setModalShow(true)}
        >
          Edit Profile
        </Button>

        <VerticallyCenteredModal
          show={modalShow}
          onHide={() => setModalShow(false)}
          author={props.author}
        />
      </div>
    );
  } else {
    return <></>;
  }
}
