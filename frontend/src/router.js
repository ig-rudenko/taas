import {createRouter} from "vue-router";

import Register from "@/components/pages/Register.vue";
import Login from "@/components/pages/Login.vue";
import Account from "@/components/pages/Account.vue";
import MyAccount from "@/components/pages/MyAccount.vue";
import AllAccounts from "@/components/pages/AllAccounts.vue";
import Home from "@/components/pages/Home.vue";
import TestsList from "@/components/pages/TestsList.vue";
import TestPassing from "@/components/pages/TestPassing.vue";
import CreateTest from "@/components/pages/CreateTest.vue";


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