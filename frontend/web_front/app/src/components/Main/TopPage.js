import React from "react";
import {useQuery, useMutation, useLazyQuery} from "@apollo/react-hooks";

import Container from '@mui/material/Container';

import styles from "./TopPage.module.css";
import {GET_PROCMANUALS} from "../../queries";



const TopPage = () => {

    const {
        loading: loadingProcmanuals,
        data: dataProcmanuals,
        error: errorProcmanuals,
    } = useQuery(GET_PROCMANUALS);

    if (loadingProcmanuals) {
        return (
            <h2>Loading Procmanual Data</h2>
        );
    }

    return (
        <Container maxWidth="lg">
            <div className={styles.announcement}>
                <h1>Procedure</h1>
                <h2>Procedure List</h2>
                {dataProcmanuals.allProcmanuals.edges.map(({ node }) => (
                    <a href="/testpage">{node.title}<br /></a>
                ))}
            </div>
        </Container>
    );
};

export default TopPage;
