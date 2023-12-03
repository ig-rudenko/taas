import { createApp } from 'vue'
import PrimeVue from "primevue/config";
import { createWebHistory } from "vue-router";
import ToastService from 'primevue/toastservice';

import "./styles.min.css"
import 'primeicons/primeicons.css'
import "primevue/resources/themes/lara-light-teal/theme.css"
import App from './App.vue'
import createRouter from "@/router.js";

import store from "@/store";
import setupInterceptors from './services/setupInterceptors';

setupInterceptors(store);
const app = createApp(App);
app.use(PrimeVue, { ripple: true });
app.use(ToastService)
app.use(store);
app.use(createRouter(createWebHistory()));
app.mount('#app');
