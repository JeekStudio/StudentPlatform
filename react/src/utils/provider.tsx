import axios, { AxiosResponse, AxiosInstance } from 'axios';
import {computed} from 'mobx';
import {getCookie} from './cookie';

const Provider: any = {
    get provider(): AxiosInstance {
        return axios.create({
            withCredentials: true,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // todo
            },
        })
    },

    getInstance(): AxiosInstance {
        return this.provider
    },

    request(...args: any) {
        return this.provider.request(...args)
    },

    post(...args: any) {
        return this.provider.post(...args)
    },

    get(...args: any) :Promise<AxiosResponse> {
        return this.provider.get(...args)
    },

    patch(...args: any) :Primise {
        return this.provider.patch(...args)
    },

    delete(...args: any) {
        return this.provider.delete(...args)
    },
};

export default Provider;