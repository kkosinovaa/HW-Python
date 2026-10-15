import React, {useEffect, useState} from 'react';
import {pizzasService} from "../services/pizzasService";
import {socketService} from "../services/socketService";
import PizzaComponent from "./PizzaComponent";
// import {client} from "websocket";

const PizzasComponent = () => {

    const [pizzas,setPizzas]=useState([])
    const [socketStatus, setSocketStatus] = useState('connecting');

    useEffect(() => {
        console.log('PizzasComponent MOUNT');
        pizzasService.getAll().then(({data})=>setPizzas(data.data))
    }, []);

    useEffect(() => {
        let client
        socketInit().then(socket=>{client=socket});
        return()=>{
            console.log('PizzasComponent UNMOUNT')
            if(client){
                client.close();


            }
        };
    },
        []);
    //  витягуємо з сокет сервісу функцію для створення вебсокету з піцами, і запускаємрц ю функцію тобто створюємо клієнт тобто сокет ззєднання
    const socketInit = async()=>{
        const {pizzas}=await socketService()

        const client= await pizzas()
        client.onopen=()=>{
            setSocketStatus('connected');
            console.log('Pizza socket connected')
              console.log('🟢 SOCKET OPEN', client);

            client.send(JSON.stringify({
                action:'subscribe_to_pizza_model_changes',
                request_id:new Date().getTime()
                            }))
        }
        const updatePizzas = (action, pizzaData) => {
    switch (action) {
        case 'create':
            setPizzas(prev => [...prev, pizzaData]);
            break;

        case 'update':
            setPizzas(prev =>
                prev.map(pizza =>
                    pizza.id === pizzaData.id ? pizzaData : pizza
                )
            );
            break;

        case 'delete':
            setPizzas(prev =>
                prev.filter(pizza => pizza.id !== pizzaData.id)
            );
            break;

        default:
            break;
    }
};

        //onmessage ми отримали повідомлення по вебсокету від беккенду бо є постійний звязок і підписка на повідомлееня від обзьорвера
        client.onmessage=({data})=>{
            const message=JSON.parse(data)
            updatePizzas(message.action,message.data)
    }
        client.onclose = () => {

             setSocketStatus('disconnected');
             console.log('CLEANUP — ****************');

}
    return client;
    }
    return (
        <div>
          <p>
    {socketStatus === 'connecting' && '🟡 Connecting...'}
    {socketStatus === 'connected' && '🟢 Connected'}
    {socketStatus === 'disconnected' && '🔴 Disconnected'}
</p>

            <div>
                {pizzas.map(pizza => <PizzaComponent key={pizza.id} pizza={pizza}/>)}
            </div>
        </div>
    );
};

export default PizzasComponent;