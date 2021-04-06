import React from 'react'
import {NavLink} from "react-router-dom";

const Navbar: React.FunctionComponent = () => {
     return(<nav>
         <div className="nav-wrapper indigo psx1">
             <a href="#" className="brand-logo">React + Typescript</a>
             <ul   className="right hide-on-med-and-down">
                 <li><NavLink to="/">Todo List</NavLink></li>
                 <li><NavLink to="/about">About us</NavLink></li>
             </ul>
         </div>
     </nav>);
}

export default Navbar;
