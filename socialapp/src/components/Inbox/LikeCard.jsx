import React, { useContext, useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Link, useNavigate } from "react-router-dom";
import useAxios from "../../utils/useAxios";
import AuthContext from "../../context/AuthContext";
import PostCard from "../Posts/PostCard";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { BsCursorFill } from "react-icons/bs";

export default function LikeCard(props) {
    // pass in the follow request object in props
    const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
    const user_id = localStorage.getItem("user_id");  // the currently logged in author
    const api = useAxios();
    const post_uuid = props.like.object.split("posts/")[1]
    //const [post, setPost] = useState([]);
    const [postsArray, setPostsArray] = useState({});
    const navigate = useNavigate();
    const routeChange = () => {
        navigate(`/authors/${props.like.author.uuid}/`);
    }
    useEffect(() => {
      api
          .get(`${baseURL}/authors/${user_id}/posts/${post_uuid}`)
          .then((response) => {
            //setPost(response.data);
            setPostsArray(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
    }, []);




  return (
    <Card className="follow-request-card">
      <Card.Header
        onClick={routeChange}
        >
        <Card.Title>
            <div className="profilePicCard">
            <img id="profilePicCard" src={props.like.author.profileImage} alt="profilePic"/>
            </div>
            <div className="text">{props.like.author.displayName}</div>
        </Card.Title>
      </Card.Header>
      <Card.Body>
          <Popup  trigger={<div> {props.like.summary} <BsCursorFill/></div>} 
          position="right center"  
          on="hover"
          mouseLeaveDelay={0}
          mouseEnterDelay={100}
          contentStyle={{ padding: '0px', border: 'none',width:'40em' ,  background:'#1c212b' }}
          arrow={true}
          >
            
            <div>
              {postsArray.length!=0
            ? 
              <PostCard 
                post = {postsArray}
                key = {postsArray.id}
              />
            
          : null}
            </div>
           
          </Popup>
        
      </Card.Body>
    </Card>
  );
}
