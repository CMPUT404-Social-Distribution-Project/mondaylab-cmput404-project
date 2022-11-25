import React from "react";
import { render } from '@testing-library/react';
import Explore from './Explore'
import { BrowserRouter } from "react-router-dom";

describe('Testing Explore page:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Explore /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});