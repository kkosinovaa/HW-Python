import React from 'react';

const PizzaComponent = ({pizza}) => {
    return (
        <div>
            <p>{pizza.name}</p>
            <p>{pizza.price}</p>
        </div>
    );
};

export default PizzaComponent;