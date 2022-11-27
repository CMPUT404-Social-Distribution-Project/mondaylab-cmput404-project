import { React } from 'react';
import "./ProfilePicture.css"

export default function ProfilePicture(props) {
  return (
    <div className="profile-pic">
        <img
        id="profilePicCard"
        src={props.profileImage || "https://upload.wikimedia.org/wikipedia/en/5/56/Joji_-_Smithereens.png"}
        alt="profilePic"
        />
    </div>
  )
}
