import {useForm} from "react-hook-form";
import {pizzasService} from "../services/pizzasService";

const PizzaForm = () => {
    const {register, handleSubmit, reset} = useForm();

    const save = async (pizza) =>{
        await pizzasService.create(pizza)
    }
    return (
        <form id={'create-new'} onSubmit={handleSubmit(save)}>
            <input type="text" placeholder={'name'} {...register('name')}/>
            <input type="text" placeholder={'size'} {...register('size')}/>
            <input type="text" placeholder={'price'} {...register('price')}/>
            <input type="text" placeholder={'days'} {...register('days')}/>
            <button>save</button>
        </form>
    );
};

export  default PizzaForm;