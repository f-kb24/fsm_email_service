import axios from 'axios'

const DEV_ENVIRONMENT = process.env.NODE_ENV === 'development'

const base = axios.create({
    baseURL: DEV_ENVIRONMENT ? 'http://localhost:4444' : '/email_service',
    timeout: 4000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
})

//     template_model: {
//         name: 'Francis',
//         total: 241.42,
//         due_date: '2022-10-14',
//         invoice_id: 1234,
//         date: '2022-08-04',
//     },

const emailAPI = {
    sendEmail: async (data: SendEmailFormDataType) => {
        try {
            console.log(data)
            const response = await base.post('/sendemail', data)
            return response.data
        } catch (err) {
            console.log(err)
        }
    },
    fetchAllTemplates: async () => {
        try {
            const response = await base.get<TemplateType[]>('/gettemplates')
            return response.data
        } catch (err) {
            console.log(err)
        }
    },
}

export default emailAPI
