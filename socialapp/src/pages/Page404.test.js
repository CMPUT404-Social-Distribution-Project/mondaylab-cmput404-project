import React from "react";
import { render } from '@testing-library/react';
import Page404 from './Page404';
import { BrowserRouter } from "react-router-dom";

describe('Testing Page404:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Page404 /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});