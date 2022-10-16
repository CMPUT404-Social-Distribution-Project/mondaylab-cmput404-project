import React from "react";
import {Container, Nav, Navbar} from "react-bootstrap";
import Logo from "../../des/logos/logo.svg";
import LogoText from "../../des/logos/logo-text.svg";
import {FaBell, FaCog} from "react-icons/fa"

function TopNavbar() {
    return (
        <Navbar bg="teal-alt" variant="dark">
            <Container fluid classname=".me-1">
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
                    <Nav.Link href="#pricing">ProfilePic</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default TopNavbar;