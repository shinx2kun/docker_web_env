import React, {useContext, useState, useRef} from "react";
import {useQuery, useMutation, useLazyQuery} from "@apollo/react-hooks";

// import { Grid } from '@mui/material';
import Container from '@mui/material/Container';
// import Button from '@mui/material/Button';
// import { DataGrid, GridToolbar } from '@mui/x-data-grid';
// import TextField from '@mui/material/TextField';
// import Dialog from '@mui/material/Dialog';
// import DialogActions from '@mui/material/DialogActions';
// import DialogContent from '@mui/material/DialogContent';
// import DialogTitle from '@mui/material/DialogTitle';
// import DeleteOutlineRoundedIcon from '@mui/icons-material/DeleteOutlineRounded';
// import HistoryIcon from '@mui/icons-material/History';
// import QrCodeIcon from '@mui/icons-material/QrCode';
// import EditOutlinedIcon from '@mui/icons-material/EditOutlined';

import styles from "./TestPage.module.css";
import {GET_RANKS} from "../../queries";

const TestPage = () => {
    // const [openDelete, setOpenDelete] = useState(false);
    // const [openEdit, setOpenEdit] = useState(false);

    const {
        loading: loadingRanks,
        data: dataRanks,
        error: Ranks,
    } = useQuery(GET_RANKS);

    if (loadingRanks) {
        return (
            <h2>Loading Event Data</h2>
        );
    } 

    console.log('dataRanks:', dataRanks.allRanks.edges);

    return (
        <Container maxWidth="lg">
            <div className={styles.announcement}>
                <h1>TestPageへようこそ！</h1>

                {/* ここにGET_RANKSの中身を表示したい */}
                <ul>
                    {dataRanks.allRanks.edges.map(({ node }) => (
                        <><li>{node.id}</li><li key={node.id}>{node.rank}</li></>
                    ))}
                </ul>
            </div>

        </Container>
    );
};

export default TestPage;
