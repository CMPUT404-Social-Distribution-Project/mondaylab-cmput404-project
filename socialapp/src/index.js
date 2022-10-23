import React from 'react';
import ReactDOM from 'react-dom/client';
import './custom_dark.scss';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import StreamHome from './pages/StreamHome';
import Inbox from './pages/Inbox';
import Explore from './pages/Explore';
import Profile from './pages/Profile';
import { AuthProvider } from "./context/AuthContext";
import Main from "./Main";
import Login from "./pages/authentication/Login";
import Register from "./pages/authentication/Register"
import AuthLayout from "./utils/AuthLayout";
import CreatePost from './components/Posts/CreatePost';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <AuthProvider>
        <Routes>
          <Route element={<AuthLayout />}>
            <Route path="/" element={<Main />}>
              <Route path='post' element={<CreatePost/>} />
              <Route path='stream' element={<StreamHome/>} />
              <Route path='inbox' element={<Inbox/>} />
              <Route path='explore' element={<Explore/>} />
              <Route path='authors/:id' element={<Profile/>} />
            </Route>
          </Route>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </AuthProvider>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
