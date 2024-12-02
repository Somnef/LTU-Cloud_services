<template>
    <div class="min-h-screen bg-gray-100">
        <!-- Navigation Bar -->
        <nav class="bg-blue-500 text-white py-4">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <h1 class="text-xl font-bold">
                    <router-link to="/" class="hover:text-gray-200">EC2 Manager</router-link>
                </h1>
                <ul class="flex space-x-4">
                    <li>
                        <router-link to="/" class="hover:text-gray-200" active-class="underline" exact>
                            Dashboard
                        </router-link>
                    </li>
                    <li>
                        <router-link to="/create" class="hover:text-gray-200" active-class="underline">
                            Create Instance
                        </router-link>
                    </li>
                </ul>
            </div>
        </nav>

        <!-- Route Content -->
        <main class="container mx-auto px-4 py-6">
            <router-view />
        </main>
    </div>
</template>

<script>
export default {
    name: "App",
};
</script>

<style>
/* Optionally, add custom styles */
</style>