import React from "react";
import { render } from '@testing-library/react';
import Profile from './Profile.js';
import { BrowserRouter } from "react-router-dom";

describe('Testing Profile:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Profile /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});