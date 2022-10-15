import React, { useState, useEffect } from 'react'
import Pusher from 'pusher-js'

const useConsole = () => {
    const [text, setText] = useState<string[]>(['Responses will be seen here'])

    const addText = (text: string) => {
        setText((prevState) => [...prevState, text])
    }

    useEffect(() => {
        Pusher.logToConsole = true

        var pusher = new Pusher('7b0d8f59bb2d205aa88f', {
            cluster: 'us3',
        })

        var channel = pusher.subscribe('fsmfrancis')
        channel.bind('email_sent', function (data: any) {
            addText(data.msg)
        })
    }, [])

    return [text, addText] as const
}
export default useConsole
