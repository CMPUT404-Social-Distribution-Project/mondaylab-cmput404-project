import React from "react";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import { useNavigate } from "react-router-dom";

export default function ProfileTabs(props) {
  const navigate = useNavigate();

  return (
    <Tabs
      defaultActiveKey="posts"
      activeKey={props.dir}
      id="uncontrolled-tab-example"
      className="mb-3"
      fill
      onSelect={(nextTab) =>
        navigate(`/authors/${props.author_id}/${nextTab}/`)
      }
    >
      <Tab eventKey="posts" title="Posts"></Tab>

      <Tab eventKey="followers" title="Followers"></Tab>

      <Tab eventKey="friends" title="Friends"></Tab>
    </Tabs>
  );
}
