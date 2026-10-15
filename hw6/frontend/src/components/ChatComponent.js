import React, {useEffect, useRef, useState} from 'react';
import {socketService} from "../services/socketService";
import {client} from "websocket";

const ChatComponent = () => {
    const [room, setRoom] = useState(null)
    const [socketClient, setSocketClient] = useState(null)
    const [messages, setMessages] = useState([])
    const roomInput = useRef()
    useEffect(() => {
        if (room) {
            socketInit(room).then(client => setSocketClient((client)))

        }
        return()=>{
            if(client){
                client.close();
            }
        };
    }, [room])

    const socketInit = async (room) => {
        const {chat} = await socketService();
        const client = await chat(room)

        client.onopen = () => {
            console.log('chat is connected')
        }
        client.onmessage=({data})=>{
            const{message, user}=JSON.parse(data.toString());
            setMessages(prevState => [...prevState,{user,message}])

        }
        return client
    }
     const roomHandler =()=>{
        setRoom(roomInput.current.value)
    }

    const handleEnterKey = (e) => {
        if (e.key == 'Enter') {
            socketClient.send(JSON.stringify({
                data: e.target.value,
                action: 'send_message',
                request_id: new Date().getTime()
            }))
            e.target.value = ''
        }
    }

    return (
        <div>
            {
                !room
                ?
                    <div>
                        <input type="text" ref={roomInput}/>
                        <button onClick={roomHandler}>Go to room</button>
                    </div>
                    :
                    <div>
                        {messages.map(msg=><div>{msg.user}: {msg.message}</div>)}
                        <input type="text" onKeyDown={handleEnterKey}/>
                    </div>
            }
        </div>
    );

};

export {ChatComponent}