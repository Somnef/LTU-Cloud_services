<template>
    <div>
        Hello
        <EC2Details :id="id" />
    </div>
  </template>
  
  <script>
  import EC2Details from "@/components/EC2/EC2Details.vue";
  
  export default {
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    components: { EC2Details },
  };
  </script>
  