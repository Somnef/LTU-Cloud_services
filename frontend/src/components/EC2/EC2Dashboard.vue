<template>
    <div class="p-6 bg-gray-100 min-h-screen">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-8">EC2 Dashboard</h1>
        <InstanceList :instances="instances" @start-instance="startInstance" @stop-instance="stopInstance" />
        <div class="flex justify-center mt-8">
            <router-link to="/create" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
                Create New Instance
            </router-link>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import InstanceList from "./InstanceList.vue";
import { EC2_API_URL } from "@/api";

export default {
    components: { InstanceList },
    data() {
        return {
            instances: [],
        };
    },
    methods: {
        fetchInstances() {
            axios.get(EC2_API_URL + "/instances")
                .then((response) => {
                    this.instances = response.data.Instances; // Update instances data
                    // console.log("Instances refreshed:", this.instances);
                })
                .catch((error) => console.error("Error fetching instances:", error));
        },
        startInstance(instanceId) {
            console.log("Attempting to start instance: ${instanceId}");

            // Change the state to hide the start button
            this.instances = this.instances.map((instance) => {
                if (instance.InstanceId === instanceId) {
                    instance.State = "pending";
                }
                return instance;
            });

            axios.post(EC2_API_URL + "/start-instance/" + instanceId)
                .then(() => {
                    console.log("Instance ${instanceId} started successfully.");
                    this.fetchInstances(); // Refresh data after starting
                })
                .catch((error) => console.error(`Failed to start instance ${instanceId}:`, error));
        },
        stopInstance(instanceId) {
            console.log("Attempting to stop instance: ${instanceId}");
            axios.post(EC2_API_URL + "/stop-instance/" + instanceId)
                .then(() => {
                    console.log("Instance ${instanceId} stopped successfully.");
                    this.fetchInstances(); // Refresh data after stopping
                })
                .catch((error) => console.error("Failed to stop instance ${instanceId}:", error));
        },
    },

    created() {
        this.fetchInstances();

        // Poll for new data every 10 seconds
        setInterval(() => {
            this.fetchInstances();
        }, 5000);
    },
};
</script>