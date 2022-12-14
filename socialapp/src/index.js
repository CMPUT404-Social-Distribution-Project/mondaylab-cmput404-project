import React from 'react';
import ReactDOM from 'react-dom/client';
import './custom_dark.scss';
import reportWebVitals from './reportWebVitals';
// import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import StreamHome from './pages/StreamHome';
import Inbox from './pages/Inbox';
import Explore from './pages/Explore';
import RemotePublicPosts from './pages/RemotePublicPosts'
import Profile from './pages/Profile';
import { AuthProvider } from "./context/AuthContext";
import Main from "./Main";
import Login from "./pages/authentication/Login";
import Register from "./pages/authentication/Register"
import AuthLayout from "./utils/AuthLayout";
import Post from "./pages/Post";
import GithubPage from "./pages/GithubPage"
import Page404 from "./pages/Page404";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Router>
      <AuthProvider>
        <Routes>
          <Route element={<AuthLayout />}>
            <Route path="/" element={<Main />}>
              <Route path="/" element={<Navigate to='stream' replace/>} />
              <Route path='stream' element={<StreamHome/>} />
              <Route path='stream/github' element={<GithubPage/>} />
              <Route path='inbox' element={<Inbox/>} />
              <Route path='explore' element={<Explore/>} />
              <Route path='remote_public_posts' element={<RemotePublicPosts/>} />
              <Route path='authors/:author_id' element={<Profile/>} />
              <Route path='authors/:author_id/:dir/' element={<Profile/>} />
              <Route path='authors/:author_id/posts/:post_id' element={<Post/>} />
              <Route path='404' element={<Page404/>} />
              <Route path="*" element={<Page404/>} />
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
