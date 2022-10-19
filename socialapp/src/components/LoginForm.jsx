import React from 'react';
import "./LoginForm.css";
import { Formik, Form } from 'formik';
import TextField from './TextField';
import * as Yup from 'yup';

export default function LoginForm({...props}) {
    const validate = Yup.object().shape({
    username: Yup.string().required('Required').max(26, 'Invalid username'),
    password: Yup.string().required(),
    });
    return (
        <Formik
            initialValues={{
                username: '',
                password: '',
            }}
            validationSchema={validate}
        >
            {formik => (
                <div>
                    <Form className='form'>
                        <h3 className="Auth-form-title">Login</h3>
                        <TextField label="Username" name="username" type="text"/>
                        <TextField label="Password" name="password" type="password"/>
                        <div className="d-grid gap-2 mt-3">
                        <button id="submit-button" type="submit" className="btn btn-primary">Submit</button>
                        </div>
                        <p id="forgot"className="forgot-password text-right mt-2">
                        Forgot your <a id="password" href="#">password?</a>
                        </p>

                        <div className="text-center">
                        New to SocialDistribution?
                        </div>
                        <div className="d-grid gap-2 mt-3">
                        <button id="signup-button" className="btn btn-primary" onClick={props.changeAuthMode}>
                            Signup
                        </button>
                        </div>

                    </Form>
                </div>
            )}
        </Formik>
    )
}
