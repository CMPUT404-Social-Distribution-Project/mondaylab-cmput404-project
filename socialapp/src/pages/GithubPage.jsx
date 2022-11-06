import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import "./pages.css";
import "./Profile.css";
import AuthContext from "../context/AuthContext";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import axios from "axios";
import { Card} from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
export default function GithubPage() {
  const { baseURL } = useContext(AuthContext); // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");
  const api = useAxios();
  const [myGithubActivities, setMyGithubActicities] = useState([]);
  const [allGithubActivities, setAllGithubActicities] = useState([]);
  const [githubName, setGithubName] = useState("");
  const [key, setKey] = useState("my");
  const routeChange = (githubName) => {
    window.open(`https://github.com/${githubName}`);
  };
  /**
   * Once the homepage starts rendering, we make an api call and get all posts owner by the current user and insert them into an array
   * however any issues or errors a logged to the console.
   *
   */
  /*
User can only see their own githubs activities */
  useEffect(() => {
    api
      .get(`${baseURL}/authors/${user_id}`)
      .then((response) => {
        if (
          response.data.github.length !== 0 &&
          response.data.github.match("[^/]+(?!.*/)")
        ) {
          let name = response.data.github.split("com/")[1];
          setGithubName(name);

          axios
            .get(`https://api.github.com/users/${name}/events`)
            .then((response) => {
              for (let data of response.data.slice(0, 10)) {
                setMyGithubActicities((prevArray) => [...prevArray, data]);
              }
            })
            .catch((error) => {
              console.log(error);
            });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  /*
User can see all githubs from all authors */
  useEffect(() => {
    api
      .get(`${baseURL}/authors`)
      .then((response) => {
        const authorList = response.data.items;
        for (let author of authorList) {
          if (
            author.github.length !== 0 &&
            author.github.match("[^/]+(?!.*/)")
          ) {
            let name = author.github.split("com/")[1];
            setGithubName(name);
            axios
              .get(`https://api.github.com/users/${name}/events`)
              .then((response) => {
                for (let data of response.data.slice(0, 10)) {
                  setAllGithubActicities((prevArray) => [...prevArray, data]);
                }
              })
              .catch((error) => {
                console.log(error);
              });
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    /**
     * We return a container that has the header and all of the posts, which are created by mapping each individual post to the PostCard js file
     * which has the format for each post object.
     *
     */

    <div className="homepage">
      <Row>
        <Col md={5}>
          <h1>GitHub Activites</h1>
        </Col>
      </Row>
      <Tabs
        id="controlled-tab-example"
        activeKey={key}
        onSelect={(k) => setKey(k)}
        className="mb-3"
        variant="pills"
        justify
      >
        <Tab eventKey="my" title="My Github">
          <div>
            {myGithubActivities.length !== 0 ? (
              myGithubActivities.map((activity, i) => (
                <Card className="post-card" key={i}>
                  <Card.Header>
                    <div
                      className="post-author"
                      onClick={() => routeChange(githubName)}
                    >
                      <div className="profile-pic-post">
                        <img src={activity.actor.avatar_url} alt="profilePic" />
                      </div>
                      <div className="post-author-name">
                        {activity.actor.login}
                      </div>
                    </div>
                  </Card.Header>

                  <Card.Body>
                    <Card.Title>
                      <ReactMarkdown>{activity.type}</ReactMarkdown>
                    </Card.Title>
                    <Card.Text>
                      <div>
                        <p> To: {activity.repo.name}</p>
                        <p>
                          Commit:
                          {typeof activity.payload.commits !== "undefined" ? (
                            activity.payload.commits[0].message
                          ) : (
                            <p> No commit message!</p>
                          )}
                        </p>
                        <p>At: {activity.created_at}</p>
                      </div>
                    </Card.Text>
                    <hr />
                  </Card.Body>
                </Card>
              ))
            ) : (
              <p>No activies.</p>
            )}
          </div>
        </Tab>
        <Tab eventKey="all" title="All Github">
          <div>
            {allGithubActivities.length !== 0 ? (
              allGithubActivities.map((activity, i) => (
                <Card className="post-card" key={i}>
                  <Card.Header>
                    <div
                      className="post-author"
                      onClick={() => routeChange(githubName)}
                    >
                      <div className="profile-pic-post">
                        <img src={activity.actor.avatar_url} alt="profilePic" />
                      </div>
                      <div className="post-author-name">
                        {activity.actor.login}
                      </div>
                    </div>
                  </Card.Header>

                  <Card.Body>
                    <Card.Title>
                      <ReactMarkdown>{activity.type}</ReactMarkdown>
                    </Card.Title>
                    <Card.Text>
                      <div>
                        <p> To: {activity.repo.name}</p>
                        <p>
                          Commit:
                          {typeof activity.payload.commits !== "undefined" ? (
                            activity.payload.commits[0].message
                          ) : (
                            <p> No commit message!</p>
                          )}
                        </p>
                        <p>At: {activity.created_at}</p>
                      </div>
                    </Card.Text>
                    <hr />
                  </Card.Body>
                </Card>
              ))
            ) : (
              <p>No activies.</p>
            )}
          </div>
        </Tab>
      </Tabs>
    </div>
  );
}
