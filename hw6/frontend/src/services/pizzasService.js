import {apiService} from "./apiService";
import {urls} from "../constants/urls";

const pizzasService={
    getAll(){
        return apiService.get(urls.pizzas)
    },
    create(data){
        return apiService.post(urls.pizzas, data)
    }
}
export {pizzasService}