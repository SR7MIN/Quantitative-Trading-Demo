import { createRouter, createWebHistory } from 'vue-router';
import login from '../components/login.vue';
import Layout from '../components/index.vue';
import sign_up from '../components/sign_up.vue';
import helloworld from '@/components/helloworld.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout
    },
    {
      path: '/hello',
      component: helloworld
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/index',
      name: 'index',
      component: Layout
    },
    {
      path: '/sign_up',
      name: 'sign_up',
      component: sign_up
    }
  ]
})

export default router
