// Definición de rutas del frontend. Cada ruta carga un componente Vue.
// Rutas más usadas: `/login`, `/operativos`, y ruta dinámica para verificar.
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from './stores/auth';
import Login from './components/Login.vue';
import Operativos from './components/Operativos.vue';
import VerificarTrabajador from './components/VerificarTrabajador.vue';
import ReportesHistorico from './components/ReportesHistorico.vue';
import Profile from './components/Profile.vue';
import Settings from './components/Settings.vue';

const routes = [
  {
    path: '/',
    redirect: '/login' // Redirigir la raíz a la página de login por defecto
  },
  {
    path: '/reportes/historico',
    name: 'ReportesHistorico',
    component: ReportesHistorico,
    // Sólo administradores pueden ver reportes históricos
    meta: { requiresAuth: true, roles: ['administrador'] }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/operativos',
    name: 'Operativos',
    component: Operativos,
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    // Ajustes sólo para administradores
    meta: { requiresAuth: true, roles: ['administrador'] }
  },
  {
    path: '/operativos/:id/verificar', // Nueva ruta dinámica
    name: 'VerificarTrabajador',
    component: VerificarTrabajador,
    // Verificación accesible a operativos, operadores y administradores
    meta: { requiresAuth: true, roles: ['operativo', 'operador', 'administrador'] }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global guard: redirect to /login when route requires auth and user not authenticated.
router.beforeEach((to, from, next) => {
  // Retrieve Pinia store at guard runtime (pinia is registered before navigation)
  const auth = useAuthStore();

  // Prevent accessing login when already authenticated
  if (to.path === '/login' && auth.isAuthenticated) {
    return next({ path: '/operativos' });
  }

  if (to.meta && to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ path: '/login', query: { redirect: to.fullPath } });
  }

  // Allow authenticated users to access the VerificarTrabajador route
  // without triggering the generic 'roles' redirect to Django admin.
  if (to.name === 'VerificarTrabajador') {
    if (to.meta && to.meta.requiresAuth && !auth.isAuthenticated) {
      return next({ path: '/login', query: { redirect: to.fullPath } });
    }
    return next();
  }

  // Si la ruta define roles, comprobar que el usuario tenga al menos uno
  if (to.meta && to.meta.roles && Array.isArray(to.meta.roles)) {
    // Allow the SPA page `ReportesHistorico` to be visited without forcing
    // a redirect to the Django admin login. If the user lacks the required
    // role for other routes, deny and send to SPA login instead.
    if (to.name === 'ReportesHistorico') {
      return next();
    }

    const allowedRoles = to.meta.roles;
    const hasRole = auth.hasAnyRole ? auth.hasAnyRole(allowedRoles) : (allowedRoles.some(r => (auth.user && auth.user.roles || []).includes(r)));
    if (!hasRole) {
      // Redirect within SPA to login instead of sending the user to Django admin.
      return next({ path: '/login', query: { redirect: to.fullPath } });
    }
  }

  return next();
});

export default router;
