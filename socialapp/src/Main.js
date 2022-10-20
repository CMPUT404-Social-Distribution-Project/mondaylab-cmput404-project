import React, { useEffect, useState } from 'react'
import SideNavBar from './components/Navbar/SideNavBar';
import TopNavBar from './components/Navbar/TopNavbar';
import { BrowserRouter as Route, Outlet} from 'react-router-dom'
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
            <Outlet />
          </div>

      </div>
      
  </div>
  )
}
