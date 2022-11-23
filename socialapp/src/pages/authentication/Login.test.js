import React from "react";
import renderer from "react-test-renderer";
import { fireEvent, render } from '@testing-library/react'
import Login from './Login.jsx'
import { BrowserRouter } from "react-router-dom";

describe('Testing Login:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Login /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});