import {createRouter} from "vue-router";

import Register from "@/components/Register.vue";
import Login from "@/components/Login.vue";
import Home from "@/components/Home.vue";
import TestsList from "@/components/TestsList.vue";
import TestPassing from "@/components/TestPassing.vue";


const routes = [
    { path: "/", component: Home },
    { path: "/tests", component: TestsList },
    { path: "/test/:id", component: TestPassing },
    { path: "/register", component: Register },
    { path: "/login", component: Login },
]

export default function (history) {
    return createRouter({
        history,
        routes
    })
}