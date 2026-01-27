import { createRouter, createWebHistory } from 'vue-router';
import Login from './components/Login.vue';
import Operativos from './components/Operativos.vue';
import VerificarTrabajador from './components/VerificarTrabajador.vue';

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
  },
  {
    path: '/operativos/:id/verificar', // Nueva ruta dinámica
    name: 'VerificarTrabajador',
    component: VerificarTrabajador
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
