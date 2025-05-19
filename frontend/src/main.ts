import {createApp} from 'vue';
import PrimeVue from "primevue/config";
import ToastService from 'primevue/toastservice';
import 'primeicons/primeicons.css';

import "@/assets/main.css";
import "@/assets/styles.min.css";
import store from "@/store";
import App from './App.vue';
import router from "@/router";
import setupInterceptors from './services/setupInterceptors';
import {Router} from "vue-router";

setupInterceptors(store);
const app = createApp(App);

app.use(PrimeVue, { ripple: true });
app.use(router);
app.config.globalProperties.$router = router as Router;

app.use(ToastService);
app.use(store);
app.mount('#app');
