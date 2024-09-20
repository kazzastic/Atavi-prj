<template>
  <div id="app">
    <PredictComponent />
    <VisualizeComponent />
  </div>
</template>

<script>
import PredictComponent from './components/PredictComponent.vue';
import VisualizeComponent from './components/VisualizeComponent.vue';

export default {
  components: {
    PredictComponent,
    VisualizeComponent,
  },
};
</script>

<style>
/* Add global styles if needed */
</style>
