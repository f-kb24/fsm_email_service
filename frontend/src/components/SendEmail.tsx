import React from 'react'
import { useState } from 'react'
import { styled } from 'theme'
import emailAPI from 'utils/api'

const SendEmail: React.FC = () => {
    const [email, setEmail] = useState<string>('')

    return (
        <Container>
            <Input value={email} onChange={(e) => setEmail(e.target.value)} />
            <Button onClick={() => emailAPI.sendEmail()}>Send Email</Button>
        </Container>
    )
}

export default SendEmail

const Container = styled.div``

const Input = styled.input``

const Button = styled.button``
