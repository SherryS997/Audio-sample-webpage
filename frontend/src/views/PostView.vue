<template>
    <div class="card mb-3" style="width: 100%; border: 2px solid #3498db; border-radius: 10px; padding: 15px;">
      <div style="position: absolute; top: 10px; right: 10px; cursor: pointer;" @click="deletePost">
        <i class="fas fa-trash" style="color: #e74c3c;"></i>
      </div>
      <h2 style="color: #2c3e50;">{{ post.title }}</h2>
      <h5 style="color: #2c3e50;">Uploader: {{ post.author }}</h5>
      <p style="color: #7f8c8d;">Description: {{ post.description }}</p>
      <h6 style="color: #7f8c8d;">Sections:</h6>
      
    <ul class="list-group" style="list-style-type: none; padding-left: 0;">
      <li v-for="(section, index) in post.sections" :key="index" style="margin-bottom: 15px; border: 1px solid #95a5a6; border-radius: 5px;">
        <h5 class="accordion-header" id="sectionHeading{{ index }}" style="background-color: #f1c40f; color: #2c3e50; padding: 10px; margin-bottom: 0;" data-bs-toggle="collapse" :data-bs-target="'#sectionCollapse' + index" aria-expanded="false" aria-controls="'sectionCollapse' + index">
          {{ section.category }} - {{ section.language }} - {{ section.gender }}
        </h5>
        <div :id="'sectionCollapse' + index" class="accordion-collapse collapse" aria-labelledby="'sectionHeading' + index">
          <div class="card-body" style="border: 1px solid #d35400; border-radius: 5px; padding: 10px;">
            <ul class="list-group" style="list-style-type: none; padding-left: 0;">
              <li v-for="(sample, sampleIndex) in section.samples" :key="sampleIndex" style="margin-bottom: 10px;">
                <p style="color: #2c3e50; margin-bottom: 5px;"><strong>Sample {{ sample.id }}</strong></p>
                <p style="color: #7f8c8d; margin-bottom: 5px;">Transcript: {{ sample.transcript }}</p>
                <p style="color: #7f8c8d; margin-bottom: 5px;">Transliteration: {{ sample.transliteration }}</p>
                <audio controls style="margin-top: 5px;">
                  <source :src="'http://tts-dc-prod.centralindia.cloudapp.azure.com:8091/static/audios/' + post.id + '/' + sample.sample_dir" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              </li>
            </ul>
          </div>
        </div>
      </li>
    </ul>
    <h3 class="mt-3">Training Data Usage:</h3>
    <canvas id="sectionChart" width="400" height="200"></canvas>
  </div>
</template>

  
  

<script>
import axios from '../../axios';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      post: {}
    }
  },
  mounted() {
    axios.get(`/api/posts/${this.$route.params.id}`)
     .then(response => {
        this.post = response.data;
        this.renderChart();
      })
     .catch(error => {
        console.error(error);
      });
  },
  methods: {
    renderChart() {
      const durations = this.post.sections.map(section => section.duration);
      const labels = this.post.sections.map(section => `${section.category} - ${section.gender.charAt(0)}`);
      
      const ctx = document.getElementById('sectionChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Duration (hours)',
            data: durations,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Duration (seconds)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Sections'
              }
            }
          }
        }
      });
    }
  }
}
</script>
