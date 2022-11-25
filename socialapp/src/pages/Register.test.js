
import React from "react";
import { render } from '@testing-library/react';
import Register from './authentication/Register';
import { BrowserRouter } from "react-router-dom";

describe('Testing Register:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Register /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});