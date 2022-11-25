import React, { useContext } from 'react';
import "./Auth.css";
import { Formik, Form } from 'formik';
import TextField from '../../components/TextField';
import * as Yup from 'yup';
import Logo from "../../des/logos/logo.svg";
import LogoText from "../../des/logos/logo-text.svg";
import AuthContext from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";


export default function Register() {
    const validate = Yup.object().shape({
        username: Yup.string().required('Required').max(128, 'Must be within 128 characters'),
        password: Yup.string().required('Required').min(8, 'Must be at least 8 characters'),
        confirmPass: Yup.string().required('Required').min(8, 'Must be at least 8 characters')
            .oneOf([Yup.ref('password'), null], 'Passwords must match'),
        github: Yup.string().url(),
        });
        

    const { registerUser } = useContext(AuthContext) || {};
    
    const navigate = useNavigate();

  return (
    <div className="Auth-form-container">
    <div className="introduction">
        <div className="Logo-container">
            <img src={Logo} alt="logo"/>
            <img 
            id="logo-text"
            alt="logo-text"
            src={LogoText} 
            />
        </div>
        <div id="intro-text" className="text-left">
            Welcome to SocialDistribution,<br/> your one stop shop for everything social media.
        </div>
    </div>
            <Formik
            initialValues={{
                username: '',
                password: '',
                confirmPass: '',
                github: '',
            }}
            validationSchema={validate}
            onSubmit={(values)=> {
                const username = values.username;
                const password = values.password;
                const github = values.github;
                registerUser(username, password, github);
            }}
        >
            {formik => (
                <div>
                <Form className='form'>
                    <h3 className="Auth-form-title">Signup</h3>
                    <div className="text-center">
                        Already registered?
                        <span id="reg-login" class="link-primary" onClick={() => navigate("/login")}>
                            Login
                        </span>
                    </div>
                    <TextField label="Username" name="username" type="text"/>
                    <TextField label="Password" name="password" type="password"/>
                    <TextField label="Confirm Password" name="confirmPass" type="password"/>
                    <TextField label="GitHub" name="github" type="text"/>
                    <button id="submit-button" type="submit" className="btn btn-primary">Submit</button>
                </Form>
            </div>
            )}
        </Formik>
</div>
  )
}
