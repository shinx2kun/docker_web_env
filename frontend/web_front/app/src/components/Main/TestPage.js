import React, {useContext, useState, useRef} from "react";
import {useQuery, useMutation, useLazyQuery} from "@apollo/react-hooks";

import { Grid } from '@mui/material';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import DeleteOutlineRoundedIcon from '@mui/icons-material/DeleteOutlineRounded';
import HistoryIcon from '@mui/icons-material/History';
import QrCodeIcon from '@mui/icons-material/QrCode';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';

import styles from "./TestPage.module.css";
import {GET_RANKS, GET_PROCMANUALS} from "../../queries";

const TestPage = () => {
    // const [openDelete, setOpenDelete] = useState(false);
    // const [openEdit, setOpenEdit] = useState(false);

    const {
        loading: loadingRanks,
        data: dataRanks,
        error: errorRanks,
    } = useQuery(GET_RANKS);

    const {
        loading: loadingProcmanuals,
        data: dataProcmanuals,
        error: errorProcmanuals,
    } = useQuery(GET_PROCMANUALS);

    if (loadingRanks) {
        return (
            <h2>Loading Rank Data</h2>
        );
    }

    if (loadingProcmanuals) {
        return (
            <h2>Loading Procmanual Data</h2>
        );
    }

    console.log('dataRanks:', dataRanks.allRanks.edges);
    console.log('dataProcmanuals:', dataProcmanuals.allProcmanuals.edges);

    return (
        <Container maxWidth="lg">
            <div className={styles.announcement}>
                <h1>TestPageへようこそ！</h1>

                {/* ここにGET_RANKSの中身を表示したい */}
                <h2>Ranks</h2>
                <ul>
                    {dataRanks.allRanks.edges.map(({ node }) => (
                        <>
                        <li>{node.id}</li>
                        <li key={node.id}>{node.rank}</li>
                        </>
                    ))}
                </ul>
                <h2>ProcManuals</h2>
                <ul>
                    {dataProcmanuals.allProcmanuals.edges.map(({ node }) => {
                        const jsonObjectCheckCmd = JSON.parse(node.checkCmd || "{}");
                        return (                        
                            <>
                            <p>・manual</p>
                            <label>ID</label>
                            <li>{node.id}</li>
                            <label>Title</label>
                            <li>{node.title}</li>
                            <label>Check Command</label>
                            {Object.entries(jsonObjectCheckCmd).map(([key, value]) => (
                                <li>
                                    <strong>{key}:</strong> {value}
                                </li>
                            ))}
                            <label>Execute Command</label>
                            <li>{node.executeCmd}</li>
                            <label>Created Date</label>
                            <li>{node.createdDate}</li>
                            </>
                        );
                    })}
                </ul>
            </div>
        </Container>
    );
};

export default TestPage;
