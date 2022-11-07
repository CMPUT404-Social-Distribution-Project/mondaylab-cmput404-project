import React, { useContext, useState } from "react";
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
            className="nav nav-pills nav-flush flex-column mb-auto text-center"
        >
            <li className="side-nav-item">
         
                <div  
                    className="create-post-button"
                    aria-current="page"
                    title="Create Post"
                    onClick={() => setNewPost(true)}
                >
                    <MdEdit />
                </div>
                {newPost && <CreatePost show={newPost} onHide={() => {setNewPost(false); refreshState(navigate, location);}}/>}

            </li>
            <li className="side-nav-item">
                <div
                    className="side-nav-link"
                    title="Stream"
                    onClick={() => navigate("/stream", {state: {refresh:true}})}
                >
                    <FaHome style={{ color: location.pathname === "/stream" ? "var(--orange)" : "var(--white-teal)" }}/>
                </div>
            </li>
            <li className="side-nav-item">
                <div
                    className="side-nav-link"
                    title="Inbox"
                    onClick={() => navigate("/inbox", {state: {refresh:true}})}
                >
                    <FaInbox style={{ color: location.pathname === "/inbox" ? "var(--orange)" : "var(--white-teal)" }}/>
                </div>
            </li>
            <li className="side-nav-item">
                <div
                    className="side-nav-link"
                    title="Explore"
                    onClick={() => navigate("/explore", {state: {refresh:true}})}
                >
                    <FaSearch style={{ color: location.pathname === "/explore" ? "var(--orange)" : "var(--white-teal)" }}/>
                </div>
            </li>
            <hr className="solid" />
            <div className="signout">
                <FaSignOutAlt 
                    onClick={() => logoutUser()}
                />
            </div>
            
        </ul>
    );
}


