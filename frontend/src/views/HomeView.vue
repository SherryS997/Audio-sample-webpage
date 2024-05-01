<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4">Recently Uploaded Samples</h2>

    <!-- Filter Section -->
    <div class="mb-4">
    <label for="language">Language:</label>
    <select v-model="language" @change="fetchFilteredData" id="language">
        <option value="">All</option>
        <option v-for="lang in languages" :key="lang" :value="lang">{{ lang }}</option>
    </select>

    <label for="gender">Gender:</label>
    <select v-model="gender" @change="fetchFilteredData" id="gender">
        <option value="">All</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
    </select>
  
    <label for="category">Category:</label>
    <select v-model="category" @change="fetchFilteredData" id="category">
        <option value="">All</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
    </select>
    </div>


    <!-- Main Content Section -->
    <main>
      <div v-for="post in filteredPosts" :key="post.id" class="card mb-4">
        <div class="card-body">
          <h3 class="card-title">{{ post.title }}</h3>
          <p class="card-text">{{ post.description }}</p>
          <router-link :to="{ name: 'post', params: { id: post.id } }" class="btn btn-primary">View Details</router-link>
        </div>
        <div class="card-footer text-muted">
          Uploaded on {{ formatDate(post.date) }} | {{ post.sample_count }} Samples
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const filteredPosts = ref([]);
const language = ref('');
const gender = ref('');
const category = ref('');
const categories = [
    'NEUTRAL',
    'HAPPY',
    'SAD',
    'ANGER',
    'FEAR',
    'SURPRISE',
    'DISGUST',
    'ALEXA',
    'DIGI',
    'BOOK',
    'CONV',
    'NEWS',
    'PROPER NOUN',
    'UMANG',
    'BB',
    ]
const languages = [
    'Hindi',
    'Assamese',
    'Bengali',
    'Bodo',
    'Dogri',
    'Gujarati',
    'Kannada',
    'Kashmiri',
    'Konkani',
    'Maithili',
    'Malayalam',
    'Marathi',
    'Manipuri',
    'Nepali',
    'Odia',
    'Punjabi',
    'Sanskrit',
    'Santali',
    'Sindhi',
    'Tamil',
    'Telugu',
    'Urdu'
];

const fetchData = async () => {
  try {
    const response = await axios.get(`/api/posts/recent?language=${language.value}&gender=${gender.value}&category=${category.value}`);
    filteredPosts.value = response.data;
  } catch (error) {
    console.error('Error fetching filtered data:', error);
  }
};

const fetchFilteredData = async () => {
  try {
    const response = await axios.get(`/api/posts/recent?language=${language.value}&gender=${gender.value}&category=${category.value}`);
    filteredPosts.value = response.data;
  } catch (error) {
    console.error('Error fetching filtered data:', error);
  }
};

onMounted(fetchData);

// Function to format date nicely
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
};
</script>

<style scoped>
  select {
      margin-right: 10px; /* Adjust this value to increase or decrease the space */
  }
</style>
