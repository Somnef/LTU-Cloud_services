<template>
    <div>
      <EC2Details :id="$route.params.id" />
    </div>
  </template>
  
  <script>
  import EC2Details from "@/components/EC2/EC2Details.vue";
  
  export default {
    components: { EC2Details },
  };
  </script>
  