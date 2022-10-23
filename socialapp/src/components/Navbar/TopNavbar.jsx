import React, { useEffect, useState, useContext } from 'react';
import {Container, Nav, Navbar} from "react-bootstrap";
import Logo from "../../des/logos/logo.svg";
import LogoText from "../../des/logos/logo-text.svg";
import {FaBell, FaCog} from "react-icons/fa"
import axios from "axios";
import AuthContext from "../../context/AuthContext";
import "./TopNavbar.css"
import default_profile_pic from "../../des/default_profile_pic.jpg";

function TopNavbar() {
    const [res, setRes] = useState("");
    const { baseURL } = useContext(AuthContext);
    // const user_id = user.user_id.split("/").pop();
    const user_id = localStorage.getItem("user_id");
  
  
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
                    <Nav.Link href="#home"><FaBell size={30}/>&emsp; </Nav.Link>
                    <Nav.Link href="#features"><FaCog size={30}/>&emsp;</Nav.Link>
                    <Nav.Link id="profilePicContainer" href="/profile">
                        <img id="profilePic" src={default_profile_pic} alt="profilepic"/>
                    </Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default TopNavbar;