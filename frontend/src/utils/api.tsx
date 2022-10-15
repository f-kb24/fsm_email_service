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

const emailAPI = {
    sendEmail: async () => {
        try {
            const data = {
                template_id: 29480074,
                template_model: {
                    nam: 'Francis',
                    total: 241.42,
                    due_date: '2022-10-14',
                    invoice_id: 1234,
                    date: '2022-08-04',
                },
                from_email: 'about@fsmfrancis.com',
                to_email: 'francis@fsmfrancis.com',
                tag: 'Invoice_for_something',
            }
            const response = await base.post('/sendemail', data)
            console.log(response)
        } catch (err) {
            console.log(err)
        }
    },
}

export default emailAPI
