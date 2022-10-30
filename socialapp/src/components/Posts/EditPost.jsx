import React, { useState, useEffect, useContext } from 'react';
import ReactMarkdown from 'react-markdown';
import { Dropdown } from 'react-bootstrap';
import { BiDotsVerticalRounded } from "react-icons/bi";
import Card from 'react-bootstrap/Card';
import AuthContext from '../../context/AuthContext';
import useAxios from "../../utils/useAxios";
import { Modal } from 'react-bootstrap';

export default function EditPost(props) {
    return (
        <Modal>
            <Modal.Title>Edit Post</Modal.Title>
        </Modal>
    )
};