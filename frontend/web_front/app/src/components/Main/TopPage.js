import React from "react";

import styles from "./TopPage.module.css";



const TopPage = () => {
    return (
        <Container maxWidth="lg">
            <div className={styles.announcement}>
                <h1>配布奉行へようこそ！</h1>
            </div>

        </Container>
    );
};

export default TopPage;
