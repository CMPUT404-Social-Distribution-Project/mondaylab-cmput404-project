import React from "react";
import {Container, Nav, Navbar} from "react-bootstrap";

function TopNavbar() {
    return (
        <Navbar bg="dark-blue" variant="dark">
            <Container fluid classname=".me-1">
                <Navbar.Brand className="me-auto">Social Distrubtion</Navbar.Brand>
                <Nav className="ml-auto">
                    <Nav.Link href="#home">Home</Nav.Link>
                    <Nav.Link href="#features">Features</Nav.Link>
                    <Nav.Link href="#pricing">Pricing</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default TopNavbar;