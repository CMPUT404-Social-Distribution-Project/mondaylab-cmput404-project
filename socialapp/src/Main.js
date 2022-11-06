import React from 'react';
import SideNavBar from './components/Navbar/SideNavBar';
import TopNavBar from './components/Navbar/TopNavbar';
import {Outlet} from 'react-router-dom'
import './custom_dark.scss';

export default function Main() {

  return (
    <div className="root-container">
      <TopNavBar />
      <div className="main">
          <SideNavBar />
          <div class="main-content-container">
            <Outlet />
          </div>
      </div>
  </div>
  )
}
