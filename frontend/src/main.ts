import { createApp } from 'vue';
import PrimeVue from "primevue/config";
import ToastService from 'primevue/toastservice';
import 'primeicons/primeicons.css';

import "@/assets/main.css";
import "@/assets/styles.min.css";
import store from "@/store";
import App from './App.vue';
import createRouter from "@/router";
import setupInterceptors from './services/setupInterceptors';

setupInterceptors(store);
const app = createApp(App);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(store);
app.use(createRouter());
app.mount('#app');
