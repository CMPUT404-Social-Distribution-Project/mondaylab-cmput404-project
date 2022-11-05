import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import AuthContext from "../context/AuthContext";
import "./pages.css";
import FollowRequestCard from "../components/Inbox/FollowRequestCard";
import LikeCard from "../components/Inbox/LikeCard";
import PostCard from "../components/Posts/PostCard";
import InboxCommentCard from '../components/Inbox/InboxCommentCard';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
export default function Inbox() {
  const [inboxItems, setInboxItems] = useState([]);      
  const [posts, setPosts] = useState([]);
  const [followRequests, setFollowRequests] = useState([]);
  const [likes, setLikes] = useState([]);
  const [comments, setComments] = useState([]);
  const { baseURL } = useContext(AuthContext);   // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id"); // the currently logged in author
  const api = useAxios();
  const [key, setKey] = useState('post');    

  function RenderInboxItem(props, type) {
    // renders a single inbox item based on its type
    if (props.item.type.toLowerCase() === "follow") {
      return <FollowRequestCard followRequest={props.item} />
    } else if (props.item.type.toLowerCase() === "like") {
      return <LikeCard like={props.item} />
    } else if (props.item.type.toLowerCase() === "comment") {
      if (props.item.author!=null){
        return <InboxCommentCard comment={props.item} />
      }
      
    } else if (props.item.type.toLowerCase() === "post") {
      return <PostCard post={props.item} />;
    }
    
  }
  
  

  useEffect(() => {
    const fetchData = async () => {
      await api      
        .get(`${baseURL}/authors/${user_id}/inbox/all`)
        .then((response) => {
          setInboxItems(response.data.items);
            for (let i = 0; i < response.data.items.length; i++) {
              if (response.data.items[i].type.toLowerCase() === "follow") {
                setFollowRequests(followRequests=>[...followRequests, response.data.items[i]] );
              } else if (response.data.items[i].type.toLowerCase() === "like") {
                setLikes(likes => [...likes, response.data.items[i]]);
              } else if (response.data.items[i].type.toLowerCase() === "comment") {
                if (response.data.items[i].author!=null){
                  setComments(comments => [...comments, response.data.items[i]]);
                }
                
              } else if (response.data.items[i].type.toLowerCase() === "post") {
                setPosts(posts => [...posts, response.data.items[i]]);
              }
              
            }


          console.log("Got inbox of author")
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
      <Tabs id="controlled-tab-example"
      activeKey={key}
      onSelect={(k) => setKey(k)}
      className="mb-3">
        <Tab eventKey="post" title="Post">
        {
        typeof posts !== 'undefined' ? 
        posts.length!==0 ?
          posts.map((item) =><PostCard post={item} />)
        :  <h4>No post yet! </h4>
          :<h4>No post yet! </h4>
        }

        
      </Tab>
      <Tab eventKey="like" title="Like">
      {
        typeof likes !== 'undefined' ? 
        likes.length!==0?
          likes.map((item) =><LikeCard like={item} />)
          : <h4>No like yet! </h4>
        : <h4>No like yet! </h4>  
        }
        
      </Tab>
      <Tab eventKey="comment" title="Comment" >
      {
        typeof comments !== 'undefined' ? 
        comments.length!==0?
          comments.map((item) =><InboxCommentCard comment={item} />)
          : <h4>No comment yet! </h4>
        : <h4>No comment yet! </h4>
        }
        
      </Tab>
      <Tab eventKey="Follow-request" title="Follow Request" >
      {
        typeof followRequests !== 'undefined'? 
        followRequests.length!==0?
          followRequests.map((item) =><FollowRequestCard followRequest={item} />)
          :<h4>No follow request yet! </h4>
        : <h4>No follow request yet! </h4>
        }
        
      </Tab>

        </Tabs>
     
      </div>
    </div>
  );
}
