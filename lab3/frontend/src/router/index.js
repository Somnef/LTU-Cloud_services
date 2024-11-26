import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "@/views/DashboardView.vue";
import InstanceDetailsView from "@/views/InstanceDetailsView.vue";
import CreateInstanceView from "@/views/CreateInstanceView.vue";

const routes = [
    { path: "/", name: "Dashboard", component: DashboardView },
    { path: "/details/:id", name: "InstanceDetails", component: InstanceDetailsView },
    { path: "/create", name: "CreateInstance", component: CreateInstanceView },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
