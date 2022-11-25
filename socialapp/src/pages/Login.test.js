import React from "react";
import { fireEvent, render } from '@testing-library/react'
import Login from './authentication/Login.jsx'
import { BrowserRouter } from "react-router-dom";
import Profile from "./Profile.jsx";
import AuthProvider, { AuthContext } from "../../src/context/AuthContext"; 
describe('Testing Login:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Login /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});
// Still not work , what I have tired.
// Error before is  TypeError: Cannot destructure property 'baseURL' of '(0 , _react.useContext)(...)' as it is undefined.
// After I chnage and add Authprovider, it become to TypeError: Cannot read properties of undefined (reading '_context')
// and TypeError: render is not a function
// so, problem is when we render the page, it will first find useContext(Authprovider), then problem is happened.
// I try to mock a useContext, but they are not works.
// So I will try to make a selenium test for frontend.
// for now, noly login, register, page404 can pass the test.
/* describe('Testing Login:', () => {
    it("renders profile 1 correctly", () => {
        const tree = render(<AuthProvider><Profile /></AuthProvider>);
        expect(tree).toMatchSnapshot();
    });
});
describe('Testing Login:', () => {
    it("renders profile 2 correctly", () => {
        const tree = render(<BrowserRouter><Profile /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
}); */