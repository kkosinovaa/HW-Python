import React, {useEffect, useRef, useState} from 'react';
import {socketService} from "../services/socketService";

const ChatComponent = () => {
    const [room, setRoom] = useState(null)
    const [socketClient, setSocketClient] = useState(null)
    const [messages, setMessages] = useState([])
    const [targetUser, setTargetUser] = useState(null)
    const [targetUsername, setTargetUsername] = useState(null)

    const roomInput = useRef()

    useEffect(() => {
        if (room) {
            socketInit(room).then(client => setSocketClient(client))
        }
    }, [room])

    const socketInit = async (room) => {
        const {chat} = await socketService()
        const client = await chat(room)

        client.onopen = () => {
            console.log('chat socket connected')
        }

        client.onmessage = ({data}) => {
            const {message, user} = JSON.parse(data.toString())

            if (user && user.includes('_')) {
                const [userId, username] = user.split('_')

                setMessages(prevState => [
                    ...prevState,
                    {
                        userId,
                        username,
                        message
                    }
                ])
            } else {
                setMessages(prevState => [
                    ...prevState,
                    {
                        user,
                        message
                    }
                ])
            }
        }

        return client
    }

    const roomHandler = () => {
        setRoom(roomInput.current.value)
    }

    const selectPrivateUser = (userId, username) => {
        if (!userId) {
            return
        }

        setTargetUser(userId)
        setTargetUsername(username)
    }

    const cancelPrivate = () => {
        setTargetUser(null)
        setTargetUsername(null)
    }

    const handleEnterKey = (e) => {
        if (e.key === 'Enter' && e.target.value.trim()) {

            if (targetUser) {
                socketClient.send(JSON.stringify({
                    data: {
                        text: e.target.value,
                        userId: targetUser
                    },
                    action: 'send_private_message',
                    request_id: new Date().getTime()
                }))
            } else {
                socketClient.send(JSON.stringify({
                    data: {
                        text: e.target.value
                    },
                    action: 'send_message',
                    request_id: new Date().getTime()
                }))
            }

            e.target.value = ''
        }
    }

    return (
        <div>
            {
                !room
                    ?
                    <div>
                        <input
                            type="text"
                            ref={roomInput}
                        />

                        <button onClick={roomHandler}>
                            Go to room
                        </button>
                    </div>

                    :

                    <div>
                        {
                            messages.map((msg, index) =>
                                <div key={index}>

                                    {
                                        msg.userId
                                            ?
                                            <>
                                                <span
                                                    onClick={() =>
                                                        selectPrivateUser(
                                                            msg.userId,
                                                            msg.username
                                                        )
                                                    }
                                                    style={{
                                                        cursor: 'pointer',
                                                        fontWeight: 'bold'
                                                    }}
                                                >
                                                    {msg.username}
                                                </span>

                                                : {msg.message}
                                            </>
                                            :
                                            msg.user
                                                ?
                                                <>
                                                    {msg.user}: {msg.message}
                                                </>
                                                :
                                                <>
                                                    {msg.message}
                                                </>
                                    }

                                </div>
                            )
                        }

                        {
                            targetUser &&
                            <div>
                                <b>
                                    Private mode  {targetUsername} (id: {targetUser})
                                </b>

                                {' '}

                                <button onClick={cancelPrivate}>
                                    Cancel
                                </button>
                            </div>
                        }

                        <input
                            type="text"
                            onKeyDown={handleEnterKey}
                        />
                    </div>
            }
        </div>
    )
}

export {ChatComponent}