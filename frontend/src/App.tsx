import SendEmail from 'components/SendEmail'
import React from 'react'
import { styled } from 'theme'

function App() {
    return (
        <Container>
            <SendEmail />
        </Container>
    )
}

export default App

const Container = styled.div`
    padding: 2rem 0rem;
    margin: 0 auto;
    max-width: 700px;
`
