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
import { authorHostIsOurs} from '../utils/utils';
import { CgRemote } from "react-icons/cg";
import ProfilePicture from '../components/ProfilePicture';

function ProfilePosts(props) {
  // console.log("PreviousUrl in ProfilePosts is", props.previousUrl);
  // console.log("NextUrl in ProfilePosts is", props.nextUrl);
  console.log("ProfilePosts posts", props.postsArray)
  return (
    <div className="posts-container-profile">
    {
      typeof props.postsArray.items !== 'undefined' ? 
        props.postsArray.items.map((post) => <PostCard 
        loggedInAuthorsLiked={props.loggedInAuthorsLiked}
        loggedInAuthorsFriends={props.loggedInAuthorsFriends} loggedInAuthorsFollowers={props.loggedInAuthorsFollowers} post={post} key={post.id}/>)
        : null
    }
      <nav>
        <ul className="pagination justify-content-center">
            { props.prevUrl &&
            <li className="page-item">
            <button className="page-link" onClick={() => props.paginationPrev()}>{'<'}</button>
            </li>
            }
            { props.nextUrl && 
            <li className="page-item">
              <button className="page-link" onClick={() => props.paginationNext()}>{'>'}</button>
            </li> 
            }
        </ul> 
      </nav>
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
  const [liked, setLiked] = useState([]);
  const { baseURL } = useContext(AuthContext);      // our api url http://127.0.0.1/service
  const { author_id, dir } = useParams();                       // gets the author id in the url
  const api = useAxios();

  const [nextUrl, setNextUrl] = useState(null);
  const [previousUrl, setPreviousURL] = useState(null);
  
  useEffect(() => {
    const loggedInUserData = async () => {
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
      await api
        .get(
          `${baseURL}/authors/${loggedInUser.uuid}/liked`
        )
        .then((response) => {
          setLiked(response.data.items);
        })
        .catch((error) => {
          console.log(error);
      });
    };
    loggedInUserData();
  }, []);

  // Called after rendering. Fetches data
  useEffect(() => {
    const fetchData = async () => {
      await axios
        .get(`${baseURL}/authors/${author_id}/`)
        .then((response) => {
          setAuthor(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
      await api      
        .get(`${baseURL}/authors/${author_id}/posts/`
        )
        .then((response) => {
          setPostsArray(response.data);
          console.log('--');
          console.log(response.data);
          setPreviousURL(response.data.previous);
          setNextUrl(response.data.next);
          console.log("previousURL IS", response.data.previous);
          console.log("nextURL IS",response.data.next);
          console.log("THE ACTUAL PREVURL IS", previousUrl)
          console.log('...');
        })
        .catch((error) => {
          console.log("Failed to get posts of author. " + error);
        });
      await api      
        .get(`${baseURL}/authors/${author_id}/followers/`
        )
        .then((response) => {
          setFollowersArray(response.data);

        })
        .catch((error) => {
          console.log("Failed to get followers of author. " + error);
        });
    };
    fetchData();
  }, [useLocation().state, dir]);

  useEffect(() => {
    console.log("URLs changed", nextUrl, previousUrl);
  }, [nextUrl, previousUrl])

  var paginationHandler = (url) => {
    console.log("url is", url);
    try{
      api.get(url)
      .then((response) => {
        setNextUrl(response.data.next);
        setPreviousURL(response.data.previous);
        setPostsArray(response.data);
      })
      .catch((error) => {
        console.log(error.response.data);
        
      });
    }
    catch (error) {
      console.log(error.response.data);
    }
  }


  return (
    <div className="profileContainer">
      <div className="profileHeader">
        <div className="profilePicWithFollowButton">
          <ProfilePicture profileImage={author.profileImage} />
          <FollowButton 
            authorViewing={author}
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
      {dir === 'posts' || dir === undefined ? 
      <ProfilePosts 
        loggedInAuthorsLiked={liked} 
        loggedInAuthorsFollowers={loggedInAuthorsFollowers} 
        loggedInAuthorsFriends={loggedInAuthorsFriends} prevUrl = {previousUrl} nextUrl={nextUrl}
      paginationPrev={() => paginationHandler(previousUrl)} paginationNext={() => paginationHandler(nextUrl)} postsArray={postsArray}/> : <></>}
      {dir === 'followers' ? <ProfileFollowers followersArray={followersArray}/> : <></>}
      {dir === 'friends' ? <ProfileFriends friendsArray={friendsArray}/> : <></>}
      

      
    </div>
  );
}
