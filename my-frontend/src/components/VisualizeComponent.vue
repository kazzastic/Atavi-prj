<template>
  <div>
    <h2>Visualize Image</h2>
    <input type="file" @change="onFileChange" accept="image/*" />
    <input type="number" v-model="confidence" placeholder="Confidence Limit" />
    <button @click="visualize">Visualize</button>
    <div v-if="resultImage">
      <h3>Result:</h3>
      <img :src="resultImage" alt="Result Image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      confidence: null,
      resultImage: null,
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async visualize() {
      if (!this.selectedFile || this.confidence === null) {
        alert("Please select an image and enter a confidence limit.");
        return;
      }

      const formData = new FormData();
      formData.append("image", this.selectedFile);
      formData.append("confidence_limit", this.confidence);

      try {
        const response = await fetch("http://127.0.0.1:8000/visualize", {
          method: "POST",
          body: formData,
        });
        
        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }

        const blob = await response.blob();
        this.resultImage = URL.createObjectURL(blob);
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while visualizing the image.");
      }
    },
  },
};
</script>

<style scoped>
/* Add any styles you want here */
</style>
