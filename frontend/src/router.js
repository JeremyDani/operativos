import { createRouter, createWebHistory } from 'vue-router';
import Login from './components/Login.vue';
import Operativos from './components/Operativos.vue'; 

const routes = [
  {
    path: '/',
    redirect: '/login' // Redirigir la raíz a la página de login por defecto
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/operativos',
    name: 'Operativos',
    component: Operativos 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
