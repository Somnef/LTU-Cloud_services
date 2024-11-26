<template>
    <div>
        Hello
    </div>
</template>

<script>
import axios from "axios";

export default {
    props: {
        id: {
            type: String,
            required: true,
        },
    },

    data() {
        return {
            instance: {},
        };
    },
    methods: {
        fetchInstance() {
            axios.get("http://127.0.0.1:5000/instance-metrics/" + this.id)
            .then((response) => {
                this.instance = response.data;
            })
            .catch((error) => console.error(error));
        },
    },
    created() {
        this.fetchInstance();
    },
};
</script>
