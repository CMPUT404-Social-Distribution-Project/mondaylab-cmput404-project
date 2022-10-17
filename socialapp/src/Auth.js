import React, { useState } from "react"
import "./Auth.css"
import Logo from "./des/logos/logo.svg";
import LogoText from "./des/logos/logo-text.svg";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';
import { Formik } from 'formik';
import LoginForm from "./components/LoginForm";
import SignupForm from "./components/SignupForm";


export default function (props) {
  let [authMode, setAuthMode] = useState("signin")

  const changeAuthMode = () => {
        setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  if (authMode === "signin") {
    return (
        <div className="Auth-form-container">
            <div className="introduction">
                <div className="Logo-container">
                    <img src={Logo} />
                    <img 
                    id="logo-text"
                    src={LogoText} 
                    />
                </div>
                <div id="intro-text" className="text-left">
                    Welcome to SocialDistribution,<br/> your one stop shop for everything social media.
                </div>
            </div>
            <LoginForm changeAuthMode={changeAuthMode}/>
        </div>
    )
  }

    return (
    <div className="Auth-form-container">
        <div className="introduction">
        <div className="Logo-container">
            <img src={Logo} />
            <img 
            id="logo-text"
            src={LogoText} 
            />
        </div>
        <div id="intro-text" className="text-left">
            Welcome to SocialDistribution,<br/> your one stop shop for everything social media.
        </div>
        </div>
        <SignupForm changeAuthMode={changeAuthMode} />
    </div>
    )
}