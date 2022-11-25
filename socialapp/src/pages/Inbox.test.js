import React from "react";
import { render } from '@testing-library/react';
import Inbox from './Inbox';
import { BrowserRouter } from "react-router-dom";

describe('Testing Inbox:', () => {
    it("renders correctly", () => {
        const tree = render(<BrowserRouter><Inbox /></BrowserRouter>);
        expect(tree).toMatchSnapshot();
    });
});