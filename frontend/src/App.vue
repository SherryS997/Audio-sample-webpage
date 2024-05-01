<script setup>
import { RouterLink, RouterView } from 'vue-router'

import { ref } from 'vue';

// Check if API key is present in local storage
const apiKey = ref(localStorage.getItem('api_key'));

// Watch for changes to the API key in local storage
window.addEventListener('storage', () => {
  apiKey.value = localStorage.getItem('api_key');
});
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-light bg-light sticky-top">
      <div class="container">
        <a class="navbar-brand" href="#">AI4Bharat</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link" exact>Home</router-link>
            </li>
            <li class="nav-item" v-if="!apiKey">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item" v-if="apiKey">
              <router-link to="/upload" class="nav-link">Upload</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
  <body>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-9">
        <RouterView />
      </div>
    </div>
  </div>
</body>
</template>

<style scoped>
/* Add any custom styles here */
.navbar-brand {
  font-weight: bold;
}

.navbar-nav .nav-link {
  font-size: 1.2rem;
}

/* Add more styles as needed */
</style>

