
import React from "react";
import renderer from "react-test-renderer";
import { fireEvent, render } from '@testing-library/react';
import Register from '../Register.jsx';
import { Axios } from "socialapp/src/utils/useAxios.js";

jest.mock(Axios)

it("renders correctly", () => {
    const tree = renderer.create(<Register/>).toJSON();
    expect(tree).toMatchSnapshot();
});