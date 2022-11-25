import React from "react";
import { render } from '@testing-library/react';
import StreamHome from './StreamHome';
import { BrowserRouter } from "react-router-dom";

describe('Testing StreamHome:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><StreamHome/></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});