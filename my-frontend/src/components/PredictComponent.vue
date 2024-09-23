<template>
  <div class="predict-container">
    <h2>Predict Bounding Boxes</h2>

    <!-- Form to upload the image and enter confidence limit -->
    <form @submit.prevent="submitPredict" class="predict-form">
      <div class="form-group">
        <label for="file-upload" class="custom-file-upload">
          Choose an image
        </label>
        <input id="file-upload" type="file" @change="onFileChange" />

        <!-- Preview section for the selected image -->
        <div v-if="fileName" class="file-preview">
          <!-- Show image preview if it's an image file -->
          <img v-if="filePreview" :src="filePreview" alt="Image Preview" class="preview-image" />
          <!-- Show the file name if it's not an image -->
          <p v-else>{{ fileName }}</p>
        </div>
      </div>

      <div class="form-group">
        <input v-model="confidence" type="number" step="0.01" placeholder="Confidence Limit" class="input-box" />
      </div>

      <button type="submit" class="submit-button">Submit</button>
    </form>

    <!-- Show predictions if available -->
    <div v-if="predictions.length" class="predictions-list">
      <h3>Predictions:</h3>
      <div v-for="(prediction, index) in predictions" :key="index" class="prediction-item">
        <p><strong>Label:</strong> {{ prediction.label }}</p>
        <p><strong>Confidence:</strong> {{ prediction.confidence.toFixed(2) }}</p>
        <p><strong>Bounding Box:</strong> [{{ prediction.bounding_box.x_min.toFixed(2) }}, {{ prediction.bounding_box.y_min.toFixed(2) }}, {{ prediction.bounding_box.x_max.toFixed(2) }}, {{ prediction.bounding_box.y_max.toFixed(2) }}]</p>
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
      fileName: "", // Holds the file name or preview
      filePreview: null, // Holds the image URL for preview
      confidence: null, // Confidence limit value
      predictions: [],
    };
  },
  methods: {
    // Handle file selection
    onFileChange(e) {
      const file = e.target.files[0];
      this.file = file;
      this.fileName = file.name;

      // Check if the selected file is an image to show the preview
      if (file && file.type.startsWith("image/")) {
        this.filePreview = URL.createObjectURL(file);
      } else {
        this.filePreview = null;
      }
    },

    // Submit the prediction request
    async submitPredict() {
      const formData = new FormData();
      formData.append("image", this.file);
      formData.append("confidence_limit", this.confidence);

      try {
        const response = await axios.post("http://34.38.123.215:8000/predict", formData, {
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

<style scoped>
/* General container styling */
.predict-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

/* Form styling */
.predict-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.custom-file-upload {
  padding: 10px 20px;
  background-color: #5c6bc0;
  color: white;
  border-radius: 5px;
  text-align: center;
  cursor: pointer;
}

input[type="file"] {
  display: none;
}

.input-box {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #d0d0d0;
  font-size: 1rem;
}

.submit-button {
  padding: 10px;
  background-color: #42a5f5;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #1e88e5;
}

/* Predictions styling */
.predictions-list {
  margin-top: 30px;
}

.prediction-item {
  background-color: #fff;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.prediction-item p {
  margin: 0;
}

h2, h3 {
  color: #424242;
}

/* File preview styling */
.file-preview {
  margin-top: 10px;
}

.preview-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
