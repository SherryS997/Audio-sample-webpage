<template>
  <div class="upload">
    <h1>Upload your files here!</h1>

    <div class="container card mb-3">
      <div class="mb-3 mt-3">
        <label for="name" class="form-label">Uploader Name</label>
        <input type="text" class="form-control" v-model="uploaderName" placeholder="XYZ">
      </div>
      <div class="mb-3">
        <label for="model-name" class="form-label">Model Name</label>
        <input type="text" class="form-control" v-model="modelName" placeholder="HiFiGAN">
      </div>
      <div class="mb-3">
        <label for="model-description" class="form-label">Model description</label>
        <textarea class="form-control" rows="3" v-model="modelDescription"></textarea>
      </div>
      <div class="mb-3">
        <label for="train-metadata" class="form-label">Upload Train Metadata</label>
        <input type="file" class="form-control form-control-lg" id="train-metadata" @change="handleTrainMetadataChange" accept=".json">
      </div>
      <div class="mb-3">
        <label for="test-metadata" class="form-label">Upload Test Metadata</label>
        <input type="file" class="form-control form-control-lg" id="test-metadata" @change="handleTestMetadataChange" accept=".json">
      </div>
      <div class="mb-3">
        <label for="files" class="form-label">Upload Audio Files</label>
        <input type="file" class="form-control form-control-lg" id="inputGroupFile" multiple @change="handleFileChange" accept=".mp3,.wav">
      </div>
      <!-- Upload button with spinner and message -->
      <button class="btn btn-primary mb-3" @click="handleSubmit" :disabled="isUploading || showSuccess">
        <span v-if="isUploading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span v-else>Upload Files</span>
        <span v-if="showSuccess" class="ms-2">Success!</span>
      </button>

      <!-- Success message -->
      <div v-if="showSuccess" class="alert alert-success" role="alert">
        Files uploaded successfully!
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../../axios.js';

export default {
  data() {
    return {
      uploaderName: '',
      modelName: '',
      modelDescription: '',
      files: [],
      trainMetadata: null,
      testMetadata: null,
      isUploading: false,
      showSuccess: false
    }
  },
  methods: {
    handleSubmit() {
      if (!this.uploaderName || !this.modelName || this.files.length === 0 || !this.trainMetadata || !this.testMetadata) {
        alert('Please fill in all required fields and select at least one audio file and metadata files');
        return;
      }

      this.isUploading = true; // Set uploading state to true

      for (let i = 0; i < this.files.length; i++) {
        if (!['audio/mp3', 'audio/wav', 'audio/mpeg'].includes(this.files[i].type)) {
          alert('Only MP3 and WAV files are allowed');
          this.resetForm(); // Reset form on error
          return;
        }
      }

      const formData = new FormData();
      formData.append('uploaderName', this.uploaderName);
      formData.append('modelName', this.modelName);
      formData.append('modelDescription', this.modelDescription);
      for (let i = 0; i < this.files.length; i++) {
        formData.append('audio ' + i, this.files[i]);
      };
      formData.append('trainMetadata', this.trainMetadata);
      formData.append('testMetadata', this.testMetadata);

      // Get API key from local storage
      const apiKey = localStorage.getItem('api_key');

      // Include API key as a header in the request
      const headers = {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${apiKey}`
      };


      axios.post('/api/samples', formData, {
        headers: headers
      })
        .then(response => {
          console.log(response);
          this.showSuccess = true; // Show success message
          this.isUploading = false; // Set uploading state to false
          this.resetForm(); // Reset form
          setTimeout(() => {
            this.$router.push({ name: 'home' }); // Redirect to home after a delay
          }, 2000); // 2 seconds delay
        })
        .catch(error => {
          console.error(error);
          this.isUploading = false; // Set uploading state to false on error
        });
    },
    handleFileChange(event) {
      this.files = event.target.files;
    },
    handleTrainMetadataChange(event) {
      this.trainMetadata = event.target.files[0];
    },
    handleTestMetadataChange(event) {
      this.testMetadata = event.target.files[0];
    },
    resetForm() {
      this.uploaderName = '';
      this.modelName = '';
      this.modelDescription = '';
      this.files = [];
      this.trainMetadata = null;
      this.testMetadata = null;
    }
  }
}
</script>
