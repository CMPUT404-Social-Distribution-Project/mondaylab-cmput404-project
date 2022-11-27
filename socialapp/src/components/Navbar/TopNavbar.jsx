import React, { useEffect, useState, useContext } from 'react';
import {Container, Nav, Navbar} from "react-bootstrap";
import Logo from "../../des/logos/logo.svg";
import LogoText from "../../des/logos/logo-text.svg";
import axios from "axios";
import AuthContext from "../../context/AuthContext";
import "./TopNavbar.css"
import { useNavigate } from "react-router-dom";
import ProfilePicture from '../ProfilePicture';

function TopNavbar() {
    const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));

    const { baseURL } = useContext(AuthContext) || {};
    const user_id = localStorage.getItem("user_id");
    const navigate = useNavigate();
    const routeChange = () => {
        navigate(`/authors/${user_id}/`, {state: {refresh:true}});
    }

    return (
        <Navbar className="topnav" bg="teal-alt" variant="dark">
            <Container fluid className=".me-1">
                <Navbar.Brand className="me-auto">
                    <img
                        src={Logo}
                        style={{ height: 50, width: 50 }}
                        alt="logo"
                    />
                    <img
                        src={LogoText}
                        style={{ height: 50, width: 250 }}
                        alt="logo-text"
                    />
                </Navbar.Brand>
                <Nav className="ml-auto" onClick={routeChange}>
                    <ProfilePicture profileImage={loggedInUser.profileImage} />
                </Nav>
            </Container>
        </Navbar>
    );
}

export default TopNavbar;