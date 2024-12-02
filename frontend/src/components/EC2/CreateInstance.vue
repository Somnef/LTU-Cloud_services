<template>
    <div class="max-w-md mx-auto p-6 border border-gray-300 rounded-lg">
        <h2 class="text-center text-2xl font-bold mb-4">Create New Instance</h2>
        <form @submit.prevent="createInstance">
            <div class="mb-4">
                <label for="instanceName" class="block text-sm font-medium text-gray-700">Instance Name:</label>
                <input type="text" id="instanceName" v-model="instanceName" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
            <div class="mb-4">
                <label for="instanceType" class="block text-sm font-medium text-gray-700">Instance Type:</label>
                <select id="instanceType" v-model="instanceType" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    <option value="" disabled>Select instance type</option>
                    <!-- <option value="t2.micro">t2.micro</option> -->
                    <option value="t3.micro">t3.micro</option>
                </select>
            </div>
            <button type="submit" class="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Create Instance</button>
        </form>
    </div>
</template>

<script>
import { EC2_API_URL } from '@/api';
import axios from 'axios';

export default {
    data() {
        return {
            instanceName: '',
            instanceType: '',
        };
    },
    methods: {
        createInstance() {
            axios.post(EC2_API_URL + '/create-instance', {
                Name: this.instanceName,
                InstanceType: this.instanceType,
            }).then(() => {
                this.$router.push('/');
            }).catch((error) => {
                console.error(error);
            });
        }
    }
};
</script>
