import React, { useEffect, useState, useContext } from "react";
import useAxios from "../utils/useAxios";
import "./pages.css";
import "./Profile.css";
import AuthContext from "../context/AuthContext";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import axios from "axios";
import { Card } from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import ReactPaginate from "react-paginate";
export default function GithubPage() {
  const { baseURL } = useContext(AuthContext) || {}; // our api url http://127.0.0.1/service
  const user_id = localStorage.getItem("user_id");
  const api = useAxios();
  const [myGithubActivities, setMyGithubActicities] = useState([]);
  const [allGithubActivities, setAllGithubActicities] = useState([]);
  const [githubName, setGithubName] = useState("");
  const [key, setKey] = useState("my");
  const routeChange = (githubName) => {
    window.open(`https://github.com/${githubName}`);
  };
  const itemsPerPage = 6;
  const [myItemOffset, setMyItemOffset] = useState(0);
  const myEndOffset = myItemOffset + itemsPerPage;
  const myGithubItems = myGithubActivities.slice(myItemOffset, myEndOffset);
  const myPageCount = Math.ceil(myGithubActivities.length / itemsPerPage);
  const [allItemOffset, setAllItemOffset] = useState(0);
  const allEndOffset = allItemOffset + itemsPerPage;
  const allGithubItems = allGithubActivities.slice(allItemOffset, allEndOffset);
  const allPageCount = Math.ceil(allGithubActivities.length / itemsPerPage);
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
              console.log("12", response.data.length);
              for (let data of response.data.slice(0, 30)) {
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
            //setGithubName(name);
            axios
              .get(`https://api.github.com/users/${name}/events`)
              .then((response) => {
                console.log("123", response.data.length);
                for (let data of response.data.slice(0, 30)) {
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

  const myHandlePageClick = (event) => {
    const myNewOffset = (event.selected * 5) % myGithubActivities.length;
    console.log(
      `User requested page number ${event.selected}, which is offset ${myNewOffset}`
    );
    setMyItemOffset(myNewOffset);
  };

  const allHandlePageClick = (event) => {
    const allNewOffset = (event.selected * 5) % allGithubActivities.length;
    console.log(
      `User requested page number ${event.selected}, which is offset ${allNewOffset}`
    );
    setAllItemOffset(allNewOffset);
  };
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
          <Row>
            {myGithubActivities.length !== 0 ? (
              myGithubItems.map((activity, i) => (
                <Col>
                  <Card className="post-card" key={i}>
                    <Card.Header>
                      <div
                        className="post-author"
                        onClick={() => routeChange(githubName)}
                      >
                        <div className="profile-pic">
                          <img
                            src={activity.actor.avatar_url}
                            alt="profilePic"
                          />
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
                </Col>
              ))
            ) : (
              <p>No activies.</p>
            )}
          </Row>
          <div style={{ marginLeft: "40%" }}>
            <ReactPaginate
              breakLabel="..."
              nextLabel="next >"
              onPageChange={myHandlePageClick}
              pageRangeDisplayed={5}
              pageCount={myPageCount}
              previousLabel="< previous"
              marginPagesDisplayed={2}
              pageClassName="page-item"
              pageLinkClassName="page-link"
              previousClassName="page-item"
              previousLinkClassName="page-link"
              nextClassName="page-item"
              nextLinkClassName="page-link"
              breakClassName="page-item"
              breakLinkClassName="page-link"
              containerClassName="pagination"
              activeClassName="active"
              renderOnZeroPageCount={null}
            />
          </div>
        </Tab>
        <Tab eventKey="all" title="All Github">
          <Row>
            {allGithubActivities.length !== 0 ? (
              allGithubItems.map((activity, i) => (
                <Col>
                  <Card className="post-card" key={i}>
                    <Card.Header>
                      <div
                        className="post-author"
                        onClick={() => routeChange(activity.actor.login)}
                      >
                        <div className="profile-pic">
                          <img
                            src={activity.actor.avatar_url}
                            alt="profilePic"
                          />
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
                </Col>
              ))
            ) : (
              <p>No activies.</p>
            )}
          </Row>
          <div style={{ marginLeft: "40%" }}>
            <ReactPaginate
              breakLabel="..."
              nextLabel="next >"
              onPageChange={allHandlePageClick}
              pageRangeDisplayed={5}
              pageCount={allPageCount}
              marginPagesDisplayed={2}
              previousLabel="< previous"
              pageClassName="page-item"
              pageLinkClassName="page-link"
              previousClassName="page-item"
              previousLinkClassName="page-link"
              nextClassName="page-item"
              nextLinkClassName="page-link"
              breakClassName="page-item"
              breakLinkClassName="page-link"
              containerClassName="pagination"
              activeClassName="active"
              renderOnZeroPageCount={null}
            />
          </div>
        </Tab>
      </Tabs>
    </div>
  );
}
