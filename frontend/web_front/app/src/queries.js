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

