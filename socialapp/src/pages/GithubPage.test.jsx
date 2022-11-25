import React from "react";
import { render } from '@testing-library/react';
import GitHubPage from './GithubPage';
import { BrowserRouter } from "react-router-dom";

describe('Testing Github Pages:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><GitHubPage /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});