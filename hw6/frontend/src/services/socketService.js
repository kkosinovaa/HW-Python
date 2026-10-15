import {authService} from "./authService";
import {w3cwebsocket as W3cwebsocket} from 'websocket'

const baseURL = process.env.REACT_APP_SOCKET_URL;

const socketService = async () => {
    const {data: {token}} = await authService.getSocketToken();
    return {
        chat: (room) => new W3cwebsocket(`${baseURL}/chat/${room}/?token=${token}`),
        pizzas: ()=> new W3cwebsocket(`${baseURL}/pizzas/?token=${token}`)
    }
}

export {
    socketService
}