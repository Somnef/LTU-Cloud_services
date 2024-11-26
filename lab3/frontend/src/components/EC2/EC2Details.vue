<template>
    <div>
        <h2>Instance Details</h2>
        <div v-if="error" class="text-red-500">{{ error }}</div>
        <div v-else-if="!instanceDetails" class="text-gray-500">Loading...</div>
        <div v-else>
            <p><strong>ID:</strong> {{ instanceDetails.InstanceId }}</p>
            
            <div class="mt-[2rem] grid grid-cols-2 gap-x-[2rem] gap-y-[4rem]">
                <div v-for="(metric, key) in instanceDetails.Metrics" :key="key">
                    <Line :data="metric.data" :options="options" />
                </div>  
            </div>

        </div>
    </div>
</template>

<script>
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'
// import * as chartConfig from './chartConfig.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default {
    props: ["id"],
    components: { Line },
    data() {
        return {
            instanceDetails: null,
            error: null,
            options: {
                responsive: true,
                maintainAspectRatio: false
            },
        };
    },
    created() {
        this.fetchInstanceDetails();

        setInterval(() => {
            this.fetchInstanceDetails();
        }, 5000);
    },
    methods: {
        async fetchInstanceDetails() {
            try {
                if (!this.id) {
                    throw new Error("Instance ID is missing");
                }
                const response = await axios.get(`http://127.0.0.1:5000/instance-metrics/${this.id}`);
                
                // add background color to data
                this.instanceDetails = response.data;

                for (let metric of this.instanceDetails.Metrics) {
                    metric.data.datasets[0].backgroundColor = 'rgba(54, 162, 235, 0.2)'
                    metric.data.datasets[0].borderColor = 'rgba(54, 162, 235, 1)'
                    metric.data.datasets[0].borderWidth = 1
                }
            } catch (err) {
                console.error("Error fetching instance details:", err);
                this.error = "Failed to load instance details.";
            }
        },
    },
};
</script>
