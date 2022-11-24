import React from "react";
import { render } from '@testing-library/react';
import TopNavBar from './TopNavbar';
import { BrowserRouter } from "react-router-dom";

describe('Testing Top NavBar:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><TopNavBar /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});