import React, { Component } from 'react';
import { Container, Nav, Navbar } from "react-bootstrap";
import "./SideNavBar.scss"
import { FaHome, FaInbox, FaSearch,  } from "react-icons/fa"
import { MdEdit } from "react-icons/md";
import { Link } from "react-router-dom";

export default class SideNavBar extends Component {
  render() {
    return (

        <ul id="sidebar" class="nav nav-pills nav-flush flex-column mb-auto text-center">
            <li class="nav-item">
                <a href="#" class="nav-link active py-3" aria-current="page" title="Create Post" data-bs-toggle="tooltip" data-bs-placement="right">
                    <MdEdit />
                </a>
            </li>
            <li>
                <Link to="/">
                    <a href="#" class="nav-link py-3" title="Stream" data-bs-toggle="tooltip" data-bs-placement="right">
                        <FaHome />
                    </a>
                </Link>
            </li>
            <li>
                <Link to="/inbox" >
                    <a href="#" class="nav-link py-3" title="Inbox" data-bs-toggle="tooltip" data-bs-placement="right">
                        <FaInbox />
                    </a>
                </Link>

            </li>
            <li>
                <Link to="/explore">
                    <a href="#" class="nav-link py-3" title="Explore" data-bs-toggle="tooltip" data-bs-placement="right">
                        <FaSearch />
                    </a>
                </Link>

            </li>
            <div class="dropdown border-top">
            <a href="#" class="d-flex align-items-center justify-content-center p-3 link-dark text-decoration-none dropdown-toggle" id="dropdownUser3" data-bs-toggle="dropdown" aria-expanded="false">
                <img src="https://github.com/mdo.png" alt="mdo" width="24" height="24" class="rounded-circle"/>
            </a>
            <ul class="dropdown-menu text-small shadow" aria-labelledby="dropdownUser3">
                <li><a class="dropdown-item" href="#">New project...</a></li>
                <li><a class="dropdown-item" href="#">Settings</a></li>
                <li><a class="dropdown-item" href="#">Profile</a></li>
                <li><a class="dropdown-item" href="#">Sign out</a></li>
            </ul>
        </div>
        </ul>

    )
  }
}

// function SideNavbar() {
//     return (
//         <Navbar bg="dark-blue" variant="dark" className="navbar navbar-dark align-items-start sidebar sidebar-dark accordion bg-gradient-primary p-0">
//             <Container fluid classname=".me-1">
//                 <Navbar.Brand className="me-auto">Social Distrubtion</Navbar.Brand>
//                 <Nav className="ml-auto">
//                     <Nav.Item>Stream</Nav.Item>
//                     <Nav.Item href="#features">Features</Nav.Item>
//                     <Nav.Item href="#pricing">Pricing</Nav.Item>
//                 </Nav>
//             </Container>
//         </Navbar>
//     );
// }