import React, { useEffect, useState } from 'react'
import StreamHome from './pages/StreamHome';
import Inbox from './pages/Inbox';
import Explore from './pages/Explore';
import Profile from './pages/Profile';
import SideNavBar from './components/Navbar/SideNavBar';
import TopNavBar from './components/Navbar/TopNavbar';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import './custom_dark.scss';
import useAxios from "./utils/useAxios";

export default function Main() {
    const [res, setRes] = useState("");
    const api = useAxios();
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await api.get("/test/");
          setRes(response.data.response);
        } catch {
          setRes("Something went wrong");
        }
      };
      fetchData();
    }, []);

  return (
    <div className="root-container">
    <TopNavBar />
    <div className="main">

        <SideNavBar />
        <div class="main-content-container">
        </div>

    </div>
  </div>
  )
}
