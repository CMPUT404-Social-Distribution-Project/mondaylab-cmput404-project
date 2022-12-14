import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import "./pages.css";
import AuthContext from "../context/AuthContext";
import axios from "axios";
import "./Profile.css";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import PostCard from "../components/Posts/PostCard";
import UserCard from "../components/UserCard";
import EditProfileButton from "../components/Profile/EditProfileButton";
import FollowButton from "../components/Profile/FollowButton";
import ProfileTabs from "../components/Profile/ProfileTabs";
import { authorHostIsOurs, extractAuthorUUID } from "../utils/utils";
import { CgRemote } from "react-icons/cg";
import ProfilePicture from "../components/ProfilePicture";
import PulseLoader from "react-spinners/PulseLoader";
import { confirmAlert } from "react-confirm-alert";
import { toast } from "react-toastify";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";

function ProfilePosts(props) {
  return (
    <div className="posts-container-profile">
      {typeof props.postsArray !== "undefined"
        ? props.postsArray.map((post) => (
            <PostCard
              loggedInAuthorsLiked={props.loggedInAuthorsLiked}
              loggedInAuthorsFriends={props.loggedInAuthorsFriends}
              loggedInAuthorsFollowers={props.loggedInAuthorsFollowers}
              post={post}
              key={post.id}
            />
          ))
        : null}
      {props.postsLoading && (
        <PulseLoader color="var(--teal)" className="profile-posts-loader" />
      )}
      {props.nextUrl && (
        <button
          className="load-more-posts-button"
          onClick={() => props.paginationNext()}
        >
          Load More Posts
        </button>
      )}
    </div>
  );
}

function ProfileFollowers(props) {
  return (
    <div className="followers-container-profile">
      {typeof props.followersArray.items !== "undefined"
        ? props.followersArray.items.map((follower, i) => (
            <div className="follower-card-and-remove">
              <UserCard author={follower} key={i} />
              {props.authorViewingIsLoggedInAuthor ? (
                <button
                  className="remove-follower-button"
                  onClick={() =>
                    props.removeFollower(extractAuthorUUID(follower.id))
                  }
                >
                  Remove Follower
                </button>
              ) : null}
            </div>
          ))
        : null}
    </div>
  );
}

function ProfileFriends(props) {
  return (
    <div className="friends-container-profile">
      {typeof props.friendsArray.items !== "undefined"
        ? props.friendsArray.items.map((friend, i) => (
            <UserCard author={friend} key={i} />
          ))
        : null}
    </div>
  );
}

export default function Profile() {
  const loggedInUser = JSON.parse(localStorage.getItem("loggedInUser"));
  const [author, setAuthor] = useState(""); // the response object we get (Author object)
  const [postsArray, setPostsArray] = useState([]);
  const [followersArray, setFollowersArray] = useState("");
  const [friendsArray, setFriendsArray] = useState("");
  const [loggedInAuthorsFollowers, setLoggedInAuthorsFollowers] = useState([]);
  const [loggedInAuthorsFriends, setLoggedInAuthorsFriends] = useState([]);
  const [liked, setLiked] = useState([]);
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const { author_id, dir } = useParams(); // gets the author id in the url
  const api = useAxios();
  const [nextUrl, setNextUrl] = useState(null);
  const [postsLoading, setPostsLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const refreshState = () => {
    navigate(`${location.pathname}`, { state: { refresh: true } });
  };

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
        .get(`${baseURL}/authors/${loggedInUser.uuid}/liked`)
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
      setPostsLoading(true);
      api
        .get(`${baseURL}/authors/${author_id}/posts/`)
        .then((response) => {
          console.log(response.data.items);
          setPostsArray(response.data.items);
          setNextUrl(response.data.next);
          setPostsLoading(false);
        })
        .catch((error) => {
          console.log("Failed to get posts of author. " + error);
        });
      api
        .get(`${baseURL}/authors/${author_id}/followers/`)
        .then((response) => {
          setFollowersArray(response.data);
        })
        .catch((error) => {
          console.log("Failed to get followers of author. " + error);
        });
      api
        .get(`${baseURL}/authors/${author_id}/friends/`)
        .then((response) => {
          setFriendsArray(response.data);
        })
        .catch((error) => {
          console.log("Failed to get followers of author. " + error);
        });
    };
    fetchData();
  }, [useLocation().state, dir]);

  var paginationHandler = (url) => {
    setPostsLoading(true);
    api
      .get(url)
      .then((response) => {
        setNextUrl(response.data.next);
        setPostsArray([...postsArray, ...response.data.items]);
        setPostsLoading(false);
      })
      .catch((error) => {
        setPostsLoading(false);
        console.log(error);
      });
  };

  const removeFollower = (followerUUID) => {
    api
      .delete(`${baseURL}/authors/${author_id}/followers/${followerUUID}`)
      .then((response) => {
        refreshState();
        toast.success("Removed follower successfully");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const confirmRemoveFollower = (followerUUID) => {
    confirmAlert({
      title: "Remove follower?",
      buttons: [
        {
          label: "Yes",
          className: "yes-button",
          onClick: () => removeFollower(followerUUID),
        },
        {
          className: "no-button",
          label: "No",
        },
      ],
    });
  };

  return (
    <div className="profileContainer">
      <SkeletonTheme
        baseColor="var(--slightly-darker-blue)"
        highlightColor="var(--dark-blue)"
      >
        <div className="profileHeader">
          <div className="profilePicWithFollowButton">
            {author ? (
              <ProfilePicture profileImage={author.profileImage} />
            ) : (
              <Skeleton circle={true} width="4rem" height="4rem" />
            )}
            {author ? (
              <FollowButton authorViewing={author} />
            ) : (
              <Skeleton width="4rem" height="1.5rem" />
            )}
          </div>

          <div className="profileInfo">
            <div className="profileName">
              {author.displayName || <Skeleton style={{lineHeight: "4.3"}} height="4rem" />}
            </div>
            {author ? (
              <div className="profileStats">
                <div id="statContainer" className="followers">
                  <span>Followers:</span>
                  {/* Issue with data not becoming fully available due to async operations;
                So just do 0 until we get the full info */}
                  <div className="infoNum">
                    {typeof followersArray.items === "undefined"
                      ? 0
                      : followersArray.items.length}
                  </div>
                </div>
                <div id="statContainer" className="friends">
                  <span>Friends:</span>
                  <div className="infoNum">
                    {typeof friendsArray.items === "undefined"
                      ? 0
                      : friendsArray.items.length}
                  </div>
                </div>
                {!authorHostIsOurs(author.host) ? (
                  <div className="host-indicator">
                    <CgRemote style={{ marginRight: "0.5em" }} />
                    {author.host}
                  </div>
                ) : (
                  <div
                    className="host-indicator"
                    style={{ background: "none" }}
                  />
                )}
              </div>
            ) : (
              <Skeleton style={{marginLeft: "1rem"}} width="25rem" height="1.5rem" />
            )}

            <EditProfileButton className="edit-button" author={author} />
          </div>
        </div>
      </SkeletonTheme>
      <ProfileTabs dir={dir} author_id={author_id} />
      {dir === "posts" || dir === undefined ? (
        <ProfilePosts
          postsLoading={postsLoading}
          loggedInAuthorsLiked={liked}
          loggedInAuthorsFollowers={loggedInAuthorsFollowers}
          loggedInAuthorsFriends={loggedInAuthorsFriends}
          nextUrl={nextUrl}
          paginationNext={() => paginationHandler(nextUrl)}
          postsArray={postsArray}
        />
      ) : (
        <></>
      )}
      {dir === "followers" ? (
        <ProfileFollowers
          removeFollower={(followerUUID) => confirmRemoveFollower(followerUUID)}
          authorViewingIsLoggedInAuthor={loggedInUser.uuid === author_id}
          followersArray={followersArray}
        />
      ) : (
        <></>
      )}
      {dir === "friends" ? (
        <ProfileFriends friendsArray={friendsArray} />
      ) : (
        <></>
      )}
    </div>
  );
}
