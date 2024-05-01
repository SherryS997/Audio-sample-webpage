import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UploadView from '../views/UploadView.vue'
import PostView from '../views/PostView.vue' // assuming you have a PostView component
import Login from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/upload',
      name: 'upload',
      component: UploadView,
      meta: { requiresAuth: true }
    },
    {
      path: '/post/:id',
      name: 'post',
      component: PostView
    },
    {
      path: '/login', 
      name: 'login',
      component: Login
    }
  ]
})

// Navigation guard to check for API key before accessing protected routes
router.beforeEach((to, from, next) => {
  const apiKey = localStorage.getItem('api_key');
  if (to.matched.some(record => record.meta.requiresAuth) && !apiKey) {
    // If the route requires authentication and API key is not present, redirect to login
    next('/login');
  } else {
    next(); // Proceed to the next route
  }
});

export default router;