import React from "react";
import renderer from "react-test-renderer";
import { fireEvent, render } from '@testing-library/react'
import Axios from "../../utils/useAxios";
import Login from './Login.jsx'

jest.mock("../../utils/useAxios")

describe('Testing Signup:', () => {
    beforeEach(() => {
        Axios.get = jest.fn().mockResolvedValue({
            startLocation: "West Edmonton Mall",
            endLocation: "UofA",
            startTime: Date(20),
            note: "Test",
        })
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it("renders correctly", () => {
        const tree = renderer.create(<Login />).toJSON();
        expect(tree).toMatchSnapshot();
    });
});