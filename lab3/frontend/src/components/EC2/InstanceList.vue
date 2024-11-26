<template>
    <div>
        <table class="table-auto w-full bg-white shadow-md rounded-lg border-collapse">
            <thead class="bg-gray-200 text-left">
                <tr>
                    <th class="p-4 border-b">Name</th>
                    <th class="p-4 border-b">Instance ID</th>
                    <th class="p-4 border-b">State</th>
                    <th class="p-4 border-b">Availability Zone</th>
                    <th class="p-4 border-b text-center">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="instance in instances" :key="instance.InstanceId" class="hover:bg-gray-50">

                    <td class="p-4 border-b">{{ instance.Name }}</td>
                    <td class="p-4 border-b">{{ instance.InstanceId }}</td>
                    <td class="p-4 border-b font-medium" :class="{
                        'text-green-600': instance.State === 'running',
                        'text-red-600': instance.State === 'stopped',
                        'text-yellow-600': instance.State === 'pending'
                    }">
                        {{ instance.State }}
                    </td>
                    <td class="p-4 border-b">{{ instance.AvailabilityZone }}</td>
                    <td class="p-4 border-b text-center">
                        <button v-if="instance.State === 'stopped'"
                            @click="$emit('start-instance', instance.InstanceId)"
                            class="bg-green-500 hover:bg-green-600 text-white py-1 px-3 rounded shadow">
                            Start
                        </button>
                        <button v-if="instance.State === 'running'" @click="$emit('stop-instance', instance.InstanceId)"
                            class="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded shadow">
                            Stop
                        </button>
                        <router-link :to="`/details/${instance.InstanceId}`" class="text-blue-500 hover:underline ml-4">
                            View Details
                        </router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    props: ["instances"],
};
</script>