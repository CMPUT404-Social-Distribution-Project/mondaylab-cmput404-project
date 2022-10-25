import React, { useContext } from "react";
import "./pages.css";
import TextField from "../components/TextField";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import useAxios from "../utils/useAxios.js";
import AuthContext from "../context/AuthContext";

export default function Explore() {
  const validate = Yup.object().shape({
    search: Yup.string(),
  });

  const api = useAxios();
  const { baseURL } = useContext(AuthContext);

  return (
    <div className="explore-container">
      <h1>Explore</h1>
      <Formik
        initialValues={{
          search: '',
        }}
        validationSchema={validate}
        onSubmit={(values) => {
          console.log(values);
          const search = values.search;

          api
            .get(`${baseURL}/authors/${search}/`)
            .then((response) => {
              // console.log(response);
              if (response.status === 200) {
                console.log(response);
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
              <TextField label="Search" name="search" type="text" />
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
    </div>
  );
}
