import React from 'react';
import ReactDOM from 'react-dom/client';
import './custom_dark.scss';
import App from './App';
import reportWebVitals from './reportWebVitals';
import TopNavBar from './components/Navbar/TopNavbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import SideNavBar from './components/Navbar/SideNavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import StreamHome from './pages/StreamHome';
import Inbox from './pages/Inbox';
import Explore from './pages/Explore';
import Profile from './pages/Profile';
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
import Auth from "./Auth"
import Main from "./Main"
import Login from "./Login"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <PrivateRoute path="/" element={<Main />} />

        </Routes>
      </AuthProvider>

    

    </Router>
    {/* <div className="root-container">
      <TopNavBar />
      <div className="main">
        <Router>
          <SideNavBar />
          <div class="main-content-container">
            <Routes>
              <Route path='/stream' element={<StreamHome/>} />
              <Route path='/inbox' element={<Inbox/>} />
              <Route path='/explore' element={<Explore/>} />
              <Route path='/profile' element={<Profile/>} />
            </Routes>
          </div>
        </Router>
      </div>
    </div> */}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
