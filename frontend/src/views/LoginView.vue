<template>
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary btn-block">Login</button>
        <!-- Error message -->
        <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
          {{ errorMessage }}
        </div>
      </form>
    </div>
  </template>
  
<script setup>
  import axios from '../../axios';
  import { ref } from 'vue';
  
  const password = ref('');
  const errorMessage = ref('');

  const login = async () => {
  try {
    const response = await axios.post('/login', { password: password.value });
    const { api_key, expires_in } = response.data;
    // Store API key and expiration time in local storage
    localStorage.setItem('api_key', api_key);
    localStorage.setItem('api_key_expires_at', Date.now() + expires_in * 1000); // Convert seconds to milliseconds
    // Redirect or perform other actions after successful login
    console.log('Logged in successfully!');

    window.location.href = '/';
  } catch (error) {
    // Display error message if login fails
    errorMessage.value = error.response.data.error;
    console.error('Login failed:', errorMessage.value);
  }

};
</script>

  <style scoped>
  .login-container {
    max-width: 320px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .login-container h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .login-form {
    width: 100%;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    font-weight: bold;
  }
  
  .btn-block {
    width: 100%;
  }
  </style>
  