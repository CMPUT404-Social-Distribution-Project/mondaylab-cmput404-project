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
    console.log(location.pathname);
    return (
        <ul
            id="sidebar"
            className="nav nav-pills nav-flush flex-column mb-auto text-center"
        >
            <li className="nav-item">
         
                <div  
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
                <div onClick={() => navigate("/stream", {state: {refresh:true}})}>
                    <div
                        className="nav-link py-3"
                        title="Stream"
                    >
                        <FaHome style={{ color: location.pathname === "/stream" || location.pathname === "/" }}/>
                    </div>
                </div>
            </li>
            <li>
                <div onClick={() => navigate("/inbox", {state: {refresh:true}})}>
                    <div
                        className="nav-link py-3"
                        title="Inbox"
                    >
                        <FaInbox style={{ color: location.pathname === "/inbox" }}/>
                    </div>
                </div>
            </li>
            <li>
                <div onClick={() => navigate("/explore", {state: {refresh:true}})}>
                    <div
                        className="nav-link py-3"
                        title="Explore"
                    >
                        <FaSearch style={{ color: location.pathname === "/explore" }}/>
                    </div>
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


