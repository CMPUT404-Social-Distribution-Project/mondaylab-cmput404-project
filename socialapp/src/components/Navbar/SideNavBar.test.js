import React from "react";
import { render } from '@testing-library/react';
<<<<<<< HEAD
import SideNavBar from './SideNavbar';
=======
import SideNavBar from './SideNavBar';
>>>>>>> 4c4581a2a221bdc6186399569d61b92a5569f7a0
import { BrowserRouter } from "react-router-dom";

describe('Testing Side NavBar:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><SideNavBar /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});