import React, { useState, useEffect } from 'react'
import emailAPI from 'utils/api'

const useSendEmail = () => {
    const [validEmail, setValidEmail] = useState(false)
    const [templates, setTemplates] = useState<TemplateType[]>([])
    const [formData, setFormData] = useState<SendEmailFormDataType>({
        template_id: null,
        template_model: {},
        from_email: 'test@fsmfrancis.com',
        to_email: '',
        tag: '',
    })

    const setEmail = (email: string) => {
        setFormData((prevState) => ({ ...prevState, to_email: email }))
        const emailRegex =
            /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/
        setValidEmail(emailRegex.test(email))
    }

    useEffect(() => {
        ;(async () => {
            const templates = await emailAPI.fetchAllTemplates()
            if (templates) {
                setTemplates(templates)
                setFormData((prevState) => ({
                    ...prevState,
                    template_id: templates[1].id,
                }))
            }
        })()
    }, [])

    return [templates, formData, setFormData, setEmail, validEmail] as const
}

export default useSendEmail
