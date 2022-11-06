import React, { Component, useContext, useState } from "react";
import { Modal, Button, InputGroup, Form } from "react-bootstrap";
import "./SideNavBar.css";
import { FaHome, FaInbox, FaSearch, FaSignOutAlt } from "react-icons/fa";
import { MdEdit } from "react-icons/md";
import { Link, useLocation, useNavigate } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import CreatePost from "../Posts/CreatePost";


export default function Sidebar() {
    const { logoutUser } = useContext(AuthContext);
    const [newPost, setNewPost] = useState(false);
    
    const navigate = useNavigate();
    const location = useLocation();

    const refreshState = (navigate, location) => {
        navigate(`${location.pathname}`, {state: {refresh:true}});
    }

    return (
        <ul
            id="sidebar"
            class="nav nav-pills nav-flush flex-column mb-auto text-center"
        >
            <li class="nav-item">
         
                <div
                    class="nav-link active py-3"
                    className="create-post-button"
                    aria-current="page"
                    title="Create Post"
                    data-bs-toggle="tooltip"
                    data-bs-placement="right"
                    onClick={() => setNewPost(true)}
                >
                    <MdEdit />
                </div>
                {newPost && <CreatePost show={newPost} onHide={() => {setNewPost(false); refreshState(navigate, location);}}/>}

            </li>
            <li>
                <Link to="/stream">
                    <a
                        href="#"
                        class="nav-link py-3"
                        title="Stream"
                        data-bs-toggle="tooltip"
                        data-bs-placement="right"
                    >
                        <FaHome />
                    </a>
                </Link>
            </li>
            <li>
                <Link to="/inbox">
                    <a
                        href="#"
                        class="nav-link py-3"
                        title="Inbox"
                        data-bs-toggle="tooltip"
                        data-bs-placement="right"
                    >
                        <FaInbox />
                    </a>
                </Link>
            </li>
            <li>
                <Link to="/explore">
                    <a
                        href="#"
                        class="nav-link py-3"
                        title="Explore"
                        data-bs-toggle="tooltip"
                        data-bs-placement="right"
                    >
                        <FaSearch />
                    </a>
                </Link>
            </li>
            <hr class="solid" />
            <div className="signout">
                <FaSignOutAlt 
                    onClick={() => logoutUser()}
                />
            </div>
            
        </ul>
    );
}


