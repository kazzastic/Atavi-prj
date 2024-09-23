<template>
  <div class="visualize-container">
    <h2>Visualize Image</h2>

    <!-- Form to upload the image and enter confidence limit -->
    <div class="visualize-form">
      <div class="form-group">
        <label for="file-upload-visualize" class="custom-file-upload">
          Choose an image
        </label>
        <input id="file-upload-visualize" type="file" @change="onFileChange" accept="image/*" />

        <!-- Preview section for the selected image -->
        <div v-if="visualizeFileName" class="file-preview">
          <!-- Show image preview if it's an image file -->
          <img v-if="visualizeFilePreview" :src="visualizeFilePreview" alt="Image Preview" class="preview-image" />
          <!-- Show the file name if it's not an image -->
          <p v-else>{{ visualizeFileName }}</p>
        </div>
      </div>

      <div class="form-group">
        <input v-model="visualizeConfidence" type="number" step="0.01" placeholder="Confidence Limit" class="input-box" />
      </div>

      <button @click="visualize" class="submit-button">Visualize</button>
    </div>

    <!-- Show the result image -->
    <div v-if="resultImage" class="result-container">
      <h3>Result:</h3>
      <img :src="resultImage" alt="Result Image" class="result-image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      visualizeFile: null,
      visualizeFileName: "", // File name for visualize component
      visualizeFilePreview: null, // Image preview for visualize component
      visualizeConfidence: null,
      resultImage: null, // Result image
    };
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      this.visualizeFile = file;
      this.visualizeFileName = file.name;

      // Check if the selected file is an image to show the preview
      if (file && file.type.startsWith("image/")) {
        this.visualizeFilePreview = URL.createObjectURL(file);
      } else {
        this.visualizeFilePreview = null;
      }
    },

    // Submit the visualize request
    async visualize() {
      if (!this.visualizeFile || this.visualizeConfidence === null) {
        alert("Please select an image and enter a confidence limit.");
        return;
      }

      const formData = new FormData();
      formData.append("image", this.visualizeFile);
      formData.append("confidence_limit", this.visualizeConfidence);

      try {
        const response = await fetch("http://34.38.123.215:8000/visualize", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }

        const blob = await response.blob();
        this.resultImage = URL.createObjectURL(blob); // Create a URL for the result image
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while visualizing the image.");
      }
    },
  },
};
</script>

<style scoped>
/* General container styling */
.visualize-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

/* Form styling */
.visualize-form {
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

/* Result image styling */
.result-container {
  margin-top: 30px;
}

.result-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2, h3 {
  color: #424242;
}
</style>
