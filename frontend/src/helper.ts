import {AxiosError} from "axios";

function HandleError(context: any, error: AxiosError<any>): void {
    let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
    context.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
}

export {HandleError}