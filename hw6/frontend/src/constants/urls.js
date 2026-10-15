const baseURL = process.env.REACT_APP_API_URL;

const auth = '/auth'
const pizzas = '/pizzas'

const urls = {
    auth: {
        login: auth,
        socket: `${auth}/socket`
    },
    pizzas
}

export {
    baseURL,
    urls
}