import React from 'react';
import ReactDOM from 'react-dom/client';
import './custom_dark.scss';
import reportWebVitals from './socialapp/src/reportWebVitals';
// import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import StreamHome from './socialapp/src/pages/StreamHome';
import Inbox from './socialapp/src/pages/Inbox';
import Explore from './socialapp/src/pages/Explore';
import Profile from './socialapp/src/pages/Profile';
import { AuthProvider } from "./socialapp/src/context/AuthContext";
import Main from "./socialapp/src/Main";
import Login from "./socialapp/src/pages/authentication/Login";
import Register from "./socialapp/src/pages/authentication/Register"
import AuthLayout from "./socialapp/src/utils/AuthLayout";
import CreatePost from './socialapp/src/components/Posts/CreatePost';
import Post from "./socialapp/src/pages/Post";
import GithubPage from "./socialapp/src/pages/GithubPage"
import Page404 from "./socialapp/src/pages/Page404";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Router>
      <AuthProvider>
        <Routes>
          <Route element={<AuthLayout />}>
            <Route path="/" element={<Main />}>
              <Route path='post' element={<CreatePost/>} />
              <Route path='stream' element={<StreamHome/>} />
              <Route path='stream/github' element={<GithubPage/>} />
              <Route path='inbox' element={<Inbox/>} />
              <Route path='explore' element={<Explore/>} />
              <Route path='authors/:author_id' element={<Profile/>} />
              <Route path='authors/:author_id/:dir/' element={<Profile/>} />
              <Route path='authors/:author_id/posts/:post_id' element={<Post/>} />
              <Route path='404' element={<Page404/>} />
            </Route>
          </Route>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </AuthProvider>
    </Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
