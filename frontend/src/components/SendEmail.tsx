import React from 'react'
import { useState } from 'react'
import { styled } from 'theme'
import emailAPI from 'utils/api'
import useConsole from './useConsole'

import useSendEmail from './useSendEmail'

const SendEmail: React.FC = () => {
    const [templates, formData, setFormData, setEmail, validEmail] =
        useSendEmail()

    const [texts, addText] = useConsole()

    const submit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const response = await emailAPI.sendEmail(formData)
        addText(response.msg)
        setEmail('')
    }

    return (
        <Container>
            <Console>
                {texts.map((text, index) => (
                    <ConsoleText key={index}>{text}</ConsoleText>
                ))}
            </Console>
            <Form onSubmit={submit}>
                <Title>Send an Email</Title>
                <InputContainer>
                    <InputTitle>Enter an Email</InputTitle>
                    <Input
                        value={formData.to_email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <Subtitle valid={validEmail}>
                        {validEmail ? 'Email is Valid' : 'Email is Invalid'}
                    </Subtitle>
                </InputContainer>
                <InputContainer>
                    <InputTitle>Select a Template</InputTitle>
                    <Select
                        onChange={(e) =>
                            setFormData((prevState) => ({
                                ...prevState,
                                template_id: parseInt(e.target.value),
                            }))
                        }
                        name="templates"
                        id="templates"
                    >
                        {templates.map((template) => (
                            <Option key={template.id} value={template.id}>
                                {template.alias}
                            </Option>
                        ))}
                    </Select>
                </InputContainer>
                <Description>
                    Email will be sent with no template models
                </Description>
                <Button disabled={!validEmail}>
                    {validEmail ? 'Send Email' : 'Enter Valid Email'}
                </Button>
            </Form>
        </Container>
    )
}

export default SendEmail

const Console = styled.div`
    width: 500px;
    border-radius: 4px;
    background-color: white;
    color: black;
    padding: 0.5rem;
    margin-bottom: 3rem;
    height: 200px;
    overflow-y: scroll;
    font-family: monospace;
    display: flex;
    flex-direction: column;
`

const ConsoleText = styled.div`
    padding: 0.2rem 0rem;
`

const Description = styled.div`
    margin: 0.3rem 0rem;
`

type SubtitleProps = {
    valid: boolean
}

const Subtitle = styled.div<SubtitleProps>`
    margin: 0.5rem 0rem;
    color: ${({ valid }) => (valid ? 'lightgreen' : 'lightcoral')};
`

const Title = styled.div`
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
`

const Form = styled.form`
    margin-bottom: 3rem;
`

const InputContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-bottom: 0.5rem;
    width: 15rem;
`
const InputTitle = styled.div`
    margin-bottom: 0.3rem;
`

const Container = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`

const Input = styled.input`
    padding: 0.3rem 0.5rem;
    font-size: 1rem;
`

const Button = styled.button`
    padding: 0.3rem 0.7rem;
    font-size: 1rem;
    cursor: pointer;
`

const Select = styled.select`
    width: 10rem;
    padding: 0.5rem;
    font-size: 1rem;
`
const Option = styled.option``
