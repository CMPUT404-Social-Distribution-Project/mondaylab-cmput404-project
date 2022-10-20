import React, { useContext } from "react";
import "./Auth.css";
import { Formik, Form } from "formik";
import TextField from "../../components/TextField";
import * as Yup from "yup";
import Logo from "../../des/logos/logo.svg";
import LogoText from "../../des/logos/logo-text.svg";
import AuthContext from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const validate = Yup.object().shape({
        username: Yup.string()
            .required("Required")
            .max(26, "Invalid username"),
        password: Yup.string().required(),
    });

    const { loginUser } = useContext(AuthContext);

    const navigate = useNavigate();

    return (
        <div className="Auth-form-container">
            <div className="introduction">
                <div className="Logo-container">
                    <img src={Logo} />
                    <img id="logo-text" src={LogoText} />
                </div>
                <div id="intro-text" className="text-left">
                    Welcome to SocialDistribution,
                    <br /> your one stop shop for everything social media.
                </div>
            </div>
            <Formik
                initialValues={{
                    username: "",
                    password: "",
                }}
                validationSchema={validate}
                onSubmit={(values) => {
                    console.log(values);
                    const username = values.username;
                    const password = values.password;
                    loginUser(username, password);
                }}
            >
                {(formik) => (
                    <div>
                        <Form className="form">
                            <h3 className="Auth-form-title">Login</h3>
                            <TextField
                                label="Username"
                                name="username"
                                type="text"
                            />
                            <TextField
                                label="Password"
                                name="password"
                                type="password"
                            />
                            <div className="d-grid gap-2 mt-3">
                                <button
                                    id="submit-button"
                                    type="submit"
                                    className="btn btn-primary"
                                >
                                    Submit
                                </button>
                            </div>
                            <p
                                id="forgot"
                                className="forgot-password text-right mt-2"
                            >
                                Forgot your{" "}
                                <a id="password" href="#">
                                    password?
                                </a>
                            </p>

                            <div className="text-center">
                                New to SocialDistribution?
                            </div>
                            <div className="d-grid gap-2 mt-3">
                                <button
                                    id="signup-button"
                                    className="btn btn-primary"
                                    onClick = {() => navigate("/register")}
                                >
                                    Signup
                                </button>
                            </div>
                        </Form>
                    </div>
                )}
            </Formik>
        </div>
    );
}
