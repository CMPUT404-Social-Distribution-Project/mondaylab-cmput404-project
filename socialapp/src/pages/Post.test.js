import React from "react";
import { render } from '@testing-library/react';
import Post from './Post';
import { BrowserRouter } from "react-router-dom";

describe('Testing Post:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Post /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});