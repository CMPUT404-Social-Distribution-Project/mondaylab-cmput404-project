import React, { useEffect, useState, useContext } from 'react'
import useAxios from "../utils/useAxios";
import AuthContext from "../context/AuthContext";
import "./pages.css";
import FollowRequestCard from "../components/Inbox/FollowRequestCard";
import LikeCard from "../components/Inbox/LikeCard";
import PostCard from "../components/Posts/PostCard";

export default function Inbox() {
  const [inboxItems, setInboxItems] = useState([]);      
  const [posts, setPosts] = useState([]);
  const [followRequests, setFollowRequests] = useState([]);
  const [likes, setLikes] = useState([]);
  const [comments, setComments] = useState([]);
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");  // the currently logged in author
  const api = useAxios();

  function RenderInboxItem(props) {
    // renders a single inbox item based on its type
    if (props.item.type.toLowerCase() === "follow") {
      return <FollowRequestCard followRequest={props.item} />
    } else if (props.item.type.toLowerCase() === "like") {
      console.log("===", props.item)
      return <LikeCard like={props.item} />
    } else if (props.item.type.toLowerCase() === "post") {
      return <PostCard post={props.item} />
    }
    
  }

  useEffect(() => {
    const fetchData = async () => {
      await api      
        .get(`${baseURL}/authors/${user_id}/inbox/all`)
        .then((response) => {
          setInboxItems(response.data.items);
          console.log("Got inbox of author")
          console.log(response.data.items);
        })
        .catch((error) => {
          console.log("Failed to get inbox of author. " + error);
        });
    };
    fetchData();
  }, []);

  return (
    <div className="inbox-container">
      <h1>Inbox</h1>
      <div className="inbox-items-container">
        {
        typeof inboxItems !== 'undefined' ? 
          inboxItems.map((item) => <RenderInboxItem item={item}/>)
          : null
        }
      </div>
    </div>
  );
}
