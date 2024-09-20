<template>
  <div>
    <h2>Predict Bounding Boxes</h2>
    <form @submit.prevent="submitPredict">
      <input type="file" @change="onFileChange" />
      <input v-model="confidence" type="number" step="0.01" placeholder="Confidence Limit" />
      <button type="submit">Submit</button>
    </form>

    <div v-if="predictions.length">
      <h3>Predictions:</h3>
      <div v-for="(prediction, index) in predictions" :key="index">
        <p>Label: {{ prediction.label }}</p>
        <p>Confidence: {{ prediction.confidence }}</p>
        <p>Bounding Box: [{{ prediction.bounding_box.x_min }}, {{ prediction.bounding_box.y_min }}, {{ prediction.bounding_box.x_max }}, {{ prediction.bounding_box.y_max }}]</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      file: null,
      confidence: 0.25, // Default confidence value
      predictions: [],
    };
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0];
    },
    async submitPredict() {
      const formData = new FormData();
      formData.append("image", this.file);
      formData.append("confidence_limit", this.confidence);

      try {
        const response = await axios.post("http://127.0.0.1:8000/predict", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        this.predictions = response.data.predictions;
      } catch (error) {
        console.error("Error submitting prediction", error);
      }
    },
  },
};
</script>
