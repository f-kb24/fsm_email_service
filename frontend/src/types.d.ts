interface TemplateType {
    id: number
    alias: string
    name: string
}

interface SendEmailFormDataType {
    template_id: number | null
    template_model: any
    from_email: string
    to_email: string
    tag: string
}