import gql from "graphql-tag";

export const GET_RANKS = gql`
query{
    allRanks {
        edges {
            node {
                id
                rank
            }
        }
    }
}
`

export const GET_PROCMANUALS = gql`
query{
    allProcmanuals {
        edges {
            node {
                id
                title
                checkCmd
                executeCmd
                createdDate
            }
        }
    }
}
`