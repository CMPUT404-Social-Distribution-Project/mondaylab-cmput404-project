import React from 'react';
import "./LoginForm.css";
import { Formik, Form } from 'formik';
import TextField from './TextField';
import * as Yup from 'yup';
import axios from 'axios';

export default function SignupForm({...props}) {
    const validate = Yup.object().shape({
        username: Yup.string().required('Required').max(26, 'Must be 26 characters or less'),
        password: Yup.string().required('Required').min(8, 'Password must be at least 8 characters'),
        confirmPass: Yup.string().required('Required')
            .min(8, 'Password must be at least 8 characters')
            .oneOf([Yup.ref('password'), null], 'Passwords must match!'),
        github: Yup.string().required('Required')
            .url('Enter a valid url')
            .matches(),

        });
    return (
        <Formik
            initialValues={{
                username: '',
                password: '',
                confirmPass: '',
                github: '',
            }}
            validationSchema={validate}
            onSubmit= {data => {
  

            }}
        >
            {formik => (
                <div>
                    <Form className='form'>
                        <h3 className="Auth-form-title">Signup</h3>
                        <div className="text-center">
                            Already registered?{" "}
                            <span id="reg-login" class="link-primary" onClick={props.changeAuthMode}>
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
    )
}
