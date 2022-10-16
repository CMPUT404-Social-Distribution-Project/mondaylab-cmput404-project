import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";

function SideNavbar() {
    return (
        <Navbar bg="dark-blue" variant="dark" className="navbar navbar-dark align-items-start sidebar sidebar-dark accordion bg-gradient-primary p-0">
            <Container fluid classname=".me-1">
                <Navbar.Brand className="me-auto">Social Distrubtion</Navbar.Brand>
                <Nav className="ml-auto">
                    <Nav.Item>Home</Nav.Item>
                    <Nav.Item href="#features">Features</Nav.Item>
                    <Nav.Item href="#pricing">Pricing</Nav.Item>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default SideNavbar;