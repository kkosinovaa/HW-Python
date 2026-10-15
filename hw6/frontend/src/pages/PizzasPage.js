import React from 'react';

import PizzasComponent from "../components/PizzasComponent";
import PizzaForm from "../components/PizzaForm";
import {ChatComponent} from "../components/ChatComponent";

const PizzasPage = () => {
    return (
        <div>
            <PizzaForm/>
            <hr/>
            <PizzasComponent/>
            <hr/>
            <ChatComponent/>
        </div>
    );
};

export default PizzasPage;