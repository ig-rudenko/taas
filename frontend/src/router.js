import {createRouter} from "vue-router";

import Register from "@/components/Register.vue";
import Login from "@/components/Login.vue";
import Account from "@/components/Account.vue";
import MyAccount from "@/components/MyAccount.vue";
import AllAccounts from "@/components/AllAccounts.vue";
import Home from "@/components/Home.vue";
import TestsList from "@/components/TestsList.vue";
import TestPassing from "@/components/TestPassing.vue";
import CreateTest from "@/components/CreateTest.vue";


const routes = [
    { path: "/", component: Home },
    { path: "/register", component: Register },
    { path: "/login", component: Login },
    { path: "/create", component: CreateTest },
    { path: "/tests", component: TestsList },
    { path: "/test/:id", component: TestPassing },
    { path: "/account", component: MyAccount },
    { path: "/account/:username", component: Account },
    { path: "/users", component: AllAccounts },
]

export default function (history) {
    return createRouter({
        history,
        routes
    })
}