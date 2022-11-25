import React from "react";
import { render } from '@testing-library/react';
import CreatePost from './CreatePost';
import { BrowserRouter } from "react-router-dom";

describe('Testing Create Post:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><CreatePost /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});