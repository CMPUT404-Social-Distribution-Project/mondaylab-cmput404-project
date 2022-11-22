
import React from "react";
import renderer from "react-test-renderer";
import { fireEvent, render } from '@testing-library/react';
import Register from './Register';
import useAxios from "../../utils/useAxios.js";

jest.mock(useAxios)

it("renders correctly", () => {
    const tree = renderer.create(<Register />).toJSON();
    expect(tree).toMatchSnapshot();
});