import React, { useEffect, useState, useContext } from 'react';
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import axios from 'axios';
import "./Profile.css";
import { useParams, useLocation } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";
import UserCard from "../components/UserCard";
import EditProfileButton from "../components/Profile/EditProfileButton";
import FollowButton from "../components/Profile/FollowButton";
import ProfileTabs from "../components/Profile/ProfileTabs";
import { authorHostIsOurs, extractAuthorUUID, createNodeObject, emptyNode } from '../utils/utils';
import { CgRemote } from "react-icons/cg";

function ProfilePosts(props) {
  return (
    <div className="posts-container-profile">
    {
      typeof props.postsArray.items !== 'undefined' ? 
        props.postsArray.items.map((post) => <PostCard loggedInAuthorsFriends={props.loggedInAuthorsFriends} loggedInAuthorsFollowers={props.loggedInAuthorsFollowers} post={post} key={post.id}/>)
        : null
    }
    </div>
  )
}

function ProfileFollowers(props) {
  return (
    <div className="followers-container-profile">
    {
      typeof props.followersArray.items !== 'undefined' ? 
        props.followersArray.items.map((follower,i) => <UserCard author={follower} key={i}/>)
        : null
    }
    </div>
  );
}

function ProfileFriends(props) {
  return (
    <div className="friends-container-profile">
    {
      typeof props.friendsArray.items !== 'undefined' ? 
        props.friendsArray.items.map((friend, i) => <UserCard author={friend} key={i}/>)
        : null
    }
    </div>
  );
}

export default function Profile() {
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const [author, setAuthor] = useState("");               // the response object we get (Author object)  
  const [postsArray, setPostsArray] = useState(""); 
  const [followersArray, setFollowersArray] = useState(""); 
  const [friendsArray, setFriendsArray] = useState(""); 
  const [loggedInAuthorsFollowers, setLoggedInAuthorsFollowers] = useState([]); 
  const [loggedInAuthorsFriends, setLoggedInAuthorsFriends] = useState([]); 
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const { author_id, dir } = useParams();                       // gets the author id in the url
  const api = useAxios();

  // node
  const [authorNode, setAuthorNode] = useState(null);     // the node object of post's author
  const [authorBaseApiURL, setAuthorBaseAPI] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      await api
        .get(`${baseURL}/authors/${loggedInUser.uuid}/followers/`)
        .then((response) => {
          setLoggedInAuthorsFollowers(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
      await api
        .get(`${baseURL}/authors/${loggedInUser.uuid}/friends/`)
        .then((response) => {
          setLoggedInAuthorsFriends(response.data.items);
        })
        .catch((error) => {
          console.log(error);
        });
    };
    fetchData();
  }, []);

  useEffect(() => {
    // first fetch the author
    const fetchAuthor = async () => {
      await axios
      .get(`${baseURL}/authors/${author_id}/`)
      .then((response) => {
        setAuthor(response.data);
        if (!authorHostIsOurs(response.data.host)) {
          // only fetch to the node if the author is ours
          fetchNode(response.data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
    }
    fetchAuthor();
  }, [useLocation().state, dir])


  const fetchNode = async (author) => {
    // fetches the node object
    await api
    .get(`${baseURL}/node/?host=${author.host}`)
    .then((response) => {
      let node = createNodeObject(response, author);
      setAuthorNode(node);
      setAuthorBaseAPI(node.host);
    })
    .catch((err) => {
      console.log(err.response.data);
    })
  }

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async (ApiURL, authorId, node) => {
      await api      
        .get(`${ApiURL}authors/${authorId}/posts/`,
        {headers: node.headers}
        )
        .then((response) => {
          setPostsArray(response.data);
        })
        .catch((error) => {
          console.log("Failed to get posts of author. " + error);
        });
      await api      
        .get(`${ApiURL}authors/${authorId}/followers/`,
        {headers: node.headers}
        )
        .then((response) => {
          setFollowersArray(response.data);

        })
        .catch((error) => {
          console.log("Failed to get followers of author. " + error);
        });
      await api      
        .get(`${ApiURL}authors/${authorId}/friends/`,
        {headers: node.headers}
        )
        .then((response) => {
          setFriendsArray(response.data);
        })
        .catch((error) => {
          console.log("Failed to get friends of author. " + error);
        });
    };
      if (!authorHostIsOurs(author.host) && authorBaseApiURL !== null) {
        console.log("THE AUTHOR IS", author);
        fetchData(authorBaseApiURL, extractAuthorUUID(author.id), authorNode);
      } else {
        // if the author is from our host, fetch from our API, or if something went wrong
        // trying to fetch the foreign author, then fetch that author from ours as backup.
        fetchData(baseURL+'/', author_id, emptyNode);
      }
      

  }, [author, authorBaseApiURL]);

  return (
    <div className="profileContainer">
      <div className="profileHeader">
        <div className="profilePicWithFollowButton">
          <div className="profilePicPage">
            <img id="profilePicPage" src={author.profileImage} alt="profilePic"/>
          </div>
          <FollowButton 
            authorViewing={author} 
            authorNode={!authorHostIsOurs(author.host) ? authorNode : emptyNode} 
            authorBaseApiURL={!authorHostIsOurs(author.host) ? authorBaseApiURL : baseURL+'/'} 
          />
        </div>

        <div className="profileInfo">
          <div className="profileName">{author.displayName}</div>
          <div className="profileStats">
            <div id="statContainer" className="followers">
              <span>Followers:</span>
              {/* Issue with data not becoming fully available due to async operations;
              So just do 0 until we get the full info */}
              <div className="infoNum">{typeof followersArray.items === 'undefined' ? 0 : followersArray.items.length}</div>
            </div>
            <div id="statContainer" className="friends">
              <span>Friends:</span>
              <div className="infoNum">{typeof friendsArray.items === 'undefined' ? 0 : friendsArray.items.length}</div>
            </div>
            {!authorHostIsOurs(author.host) ? 
            <div className="host-indicator">
              <CgRemote style={{marginRight:"0.5em"}}/>{author.host}</div> : <div className="host-indicator" style={{background: "none"}}/>}
          </div>
          <EditProfileButton className="edit-button" author={author}/>
        </div>
      </div>
      <ProfileTabs dir={dir} author_id={author_id}/>
      {dir === 'posts' || dir === undefined ? <ProfilePosts loggedInAuthorsFollowers={loggedInAuthorsFollowers} loggedInAuthorsFriends={loggedInAuthorsFriends} postsArray={postsArray}/> : <></>}
      {dir === 'followers' ? <ProfileFollowers followersArray={followersArray}/> : <></>}
      {dir === 'friends' ? <ProfileFriends friendsArray={friendsArray}/> : <></>}

    </div>
  );
}
