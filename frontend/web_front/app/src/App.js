import React from "react";
// import styles from "./App.module.css";
import {ApolloProvider} from '@apollo/react-hooks';
import {ApolloClient, InMemoryCache} from "@apollo/client";
import {Route, BrowserRouter, Switch} from "react-router-dom";

import TestPage from "./components/Main/TestPage";
// import TopPage from "./components/Main/TopPage";
// import Auth from "./components/Auth/Auth";
// import MainPage from "./components/Main/MainPage";
// import StateContextProvider from "./context/StateContext";



const client = new ApolloClient({
  uri: "http://127.0.0.1:8080/graphql/",
  headers: {
    authorization: localStorage.getItem("token") ? `JWT ${localStorage.getItem("token")}` : "",
  },
  cache: new InMemoryCache(),
});
function App() {
  return (
    <ApolloProvider client={client}>
      {/* <StateContextProvider> */}
        {/* <div className={styles.app}> */}
        <div>
            <BrowserRouter>
                <Switch>
                    <Route exact path="/" component={TestPage} />
                    {/* <Route exact path="/" component={TopPage} />
                    <Route exact path="/" component={Auth} />
                    <Route exact path="/employees" component={MainPage} /> */}
                </Switch>
            </BrowserRouter>
        </div>
      {/* </StateContextProvider> */}
    </ApolloProvider>
  );
}

export default App;
