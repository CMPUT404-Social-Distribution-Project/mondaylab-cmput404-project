import React, { useEffect, useState, useContext } from 'react';
import {Container, Nav, Navbar} from "react-bootstrap";
import Logo from "../../des/logos/logo.svg";
import LogoText from "../../des/logos/logo-text.svg";
import axios from "axios";
import AuthContext from "../../context/AuthContext";
import "./TopNavbar.css"
import { useNavigate } from "react-router-dom";

function TopNavbar() {
    const [res, setRes] = useState("");
    const { baseURL } = useContext(AuthContext);
    const user_id = localStorage.getItem("user_id");
    const navigate = useNavigate();
    const routeChange = () => {
        navigate(`/authors/${user_id}/`, {state: {refresh:true}});
    }
  
    // Called after rendering. Fetches data
    useEffect(() => {
      const fetchData = async () => {
        axios
          .get(baseURL + `/authors/${user_id}/`)
          .then((response) => {
            console.log(response.data);
            setRes(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
      };
      fetchData();
    }, []);

    return (
        <Navbar id="topnav" bg="teal-alt" variant="dark">
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
                <Nav className="ml-auto">
                    {/* <Nav.Link href="#features"><FaCog size={30}/>&emsp;</Nav.Link> */}
                    <span id="profilePicContainer" onClick={routeChange}
                    >
                        <img id="profilePic" src={res.profileImage} alt="profilepic"/>
                    </span>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default TopNavbar;