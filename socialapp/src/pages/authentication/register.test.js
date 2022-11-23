
import React from "react";
import renderer from "react-test-renderer";
import { fireEvent, render } from '@testing-library/react';
import Register from './Register';
import { AuthProvider } from "../../context/AuthContext";
import { Route, BrowserRouter } from "react-router-dom";

describe('Testing Register:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Register /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});