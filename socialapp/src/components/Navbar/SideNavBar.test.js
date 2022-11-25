import React from "react";
import { render } from '@testing-library/react';
import SideNavBar from './SideNavbar';
import { BrowserRouter } from "react-router-dom";

describe('Testing Side NavBar:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><SideNavBar /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});