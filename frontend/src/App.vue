<template>
  <!-- Contenedor principal de la app: envuelve header y main -->
  <div id="app-container">
    <header v-if="!hideHeader">
      <nav>
        <!-- Imagen de marca/país usando flag.png desde public -->
        <img src="/flag.png" alt="Venezuela" class="brand-flag" />
        
        <!-- Agrupar acciones y perfil en la sección derecha -->
        <div class="right-actions" :class="{ 'shift-left-20': route.path === '/operativos' }" v-if="route.path !== '/login'">
          <div class="nav-actions">
            <!-- Enlace al login: sólo visible cuando no hay sesión -->
            <router-link to="/login" v-if="!authStore.isAuthenticated">Login</router-link>
            <!-- Cuando el usuario está autenticado mostramos iconos (Reporte, Inicio) -->
            <span v-if="authStore.isAuthenticated" class="icon-nav">
              <!-- Icono Calendario (antes del icono de reportes, mismo estilo) -->
              <router-link
                v-if="authStore.isAuthenticated && (isAdmin || (!isOperador && (!authStore.user.roles || authStore.user.roles.length === 0)))"
                to="/operativos"
                class="icon-link calendar-link"
                title="Calendario de operativos"
                @click="onCalendarClick"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-calendar">
                  <rect x="4" y="5" width="16" height="16" rx="2" ry="2"></rect>
                  <line x1="4" y1="10" x2="20" y2="10"></line>
                  <line x1="8" y1="3" x2="8" y2="7"></line>
                  <line x1="16" y1="3" x2="16" y2="7"></line>
                </svg>
                <span class="calendar-text">Calendario</span>
              </router-link>

              <!-- Icono Reportes (visible para administradores y usuarios sin roles, pero no para operadores) -->
              <router-link
                v-if="authStore.isAuthenticated && (isAdmin || (!isOperador && (!authStore.user.roles || authStore.user.roles.length === 0)))"
                to="/reportes/historico"
                class="icon-link report-link"
                title="Reportes"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-file-text"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line></svg>
                <span class="report-text">Reporte</span>
              </router-link>

              <!-- Icono Inicio (junto a acciones) -->
              <router-link to="/operativos" class="icon-link home-link" title="Inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1V9.5z"></path></svg>
                <span class="home-text">Inicio</span>
              </router-link>

            </span>
          </div>

          <!-- Perfil al extremo derecho dentro de right-actions -->
          <div class="profile-wrapper" ref="profileRef">
              <button class="icon-link profile-link" @click="toggleMenu" title="Perfil">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              <span class="username">{{ authStore.user.nombre }}</span>
            </button>

            <div v-if="menuOpen" class="profile-menu">
              <router-link to="/perfil" class="menu-item" @click="closeMenu">Ver Perfil</router-link>
              <router-link to="/settings" class="menu-item" @click="closeMenu">Ajustes</router-link>
              <button class="menu-item logout" @click="doLogout">Cerrar sesión</button>
            </div>
          </div>
        </div>
      </nav>
    </header>
    <main>
      <!-- Punto de montaje dinámico para las vistas del router -->
      <router-view />
    </main>
  </div>
</template>

<script setup>
// `authState` es el estado reactivo compartido (módulo `auth.js`) que
// controla si el usuario está autenticado. Es usado en la plantilla
// para mostrar/ocultar enlaces de navegación.
import { computed, watch } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();

// Current route (used to hide header actions on the login route)
const route = useRoute();

// Pinia auth store to drive UI state
const authStore = useAuthStore();
// Indica si el usuario autenticado pertenece al rol "operador"
const isOperador = computed(() => authStore.user && Array.isArray(authStore.user.roles) && authStore.user.roles.includes('operador'));
// Indica si el usuario autenticado pertenece al rol "administrador"
const isAdmin = computed(() => authStore.user && Array.isArray(authStore.user.roles) && authStore.user.roles.includes('administrador'));

// Oculta completamente el header solo cuando estamos en /login
// y el parámetro redirect apunta a una ruta de verificación de operativo
const hideHeader = computed(() => {
  if (route.path !== '/login') return false;
  const redirect = route.query.redirect;
  if (typeof redirect !== 'string') return false;
  return /\/operativos\/\d+\/verificar/.test(redirect);
});

// Debug: registra en consola cuando cambia el estado de autenticación
watch(() => authStore.isAuthenticated, (val) => {
  console.debug('App: authStore.isAuthenticated ->', val, authStore.user);
});

// Cierra la sesión usando el store y redirige al login
function logout() {
  authStore.clear();
  router.push('/login');
}

import { ref, onMounted, onBeforeUnmount } from 'vue';

// Controla si el menú desplegable del perfil está abierto
const menuOpen = ref(false);
// Referencia al contenedor del perfil para detectar clics fuera
const profileRef = ref(null);

// Alterna la visibilidad del menú de perfil cuando se hace clic en el botón
function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

// Cierra el menú de perfil (se usa desde varias funciones)
function closeMenu() {
  menuOpen.value = false;
}

// Detecta clics globales para cerrar el menú cuando se hace clic fuera del perfil
function handleDocumentClick(e) {
  if (!profileRef.value) return;
  if (!profileRef.value.contains(e.target)) {
    closeMenu();
  }
}

// Maneja el clic en el icono de calendario del header.
// Si ya estamos en /operativos, envía un evento global que la vista
// de Operativos escucha para mostrar/ocultar su calendario.
function onCalendarClick() {
  if (route.path === '/operativos') {
    window.dispatchEvent(new CustomEvent('toggle-operativos-calendar'));
  }
}

// Registra y limpia el listener global de clics cuando se monta/desmonta el componente
onMounted(() => document.addEventListener('click', handleDocumentClick));
onBeforeUnmount(() => document.removeEventListener('click', handleDocumentClick));

// Cierra el menú de perfil, limpia la sesión y redirige al login
function doLogout() {
  // Close menu and logout via Pinia store
  closeMenu();
  authStore.clear();
  router.push('/login');
}

const __script = {}; // keep linter happy
</script>

<style scoped>
#app-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

main {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 50px;
  /* Altura la controla cada vista (Operativos ya usa 100vh) */
  min-height: auto;
  /* Dejar transparente para que cada vista (por ejemplo Operativos) pinte su propio fondo */
  background-color: transparent;
}

header {
  background-color: #fff;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.brand-flag { height: 28px; margin-right: 12px; vertical-align: middle; }

.icon-nav{display:inline-flex;gap:0;align-items:center;margin-left:12px;transform:translateX(-30px);transition:transform 180ms ease}
.icon-link{color:#333;display:inline-flex;align-items:center;padding:6px 6px;position:relative}
.icon-link svg{display:block}
/* small spacing for header */
.nav-actions{display:flex;align-items:center;gap:12px;justify-content:flex-end}
/* Right-side container to push actions to the far right */
.right-actions{margin-left:auto;display:flex;align-items:center;gap:12px}
/* Shift right-actions slightly left on specific routes (reduced to avoid overlap) */
.right-actions.shift-left-20{transform:translateX(-6px);transition:transform 180ms ease;z-index:1100}
nav{display:flex;align-items:center;gap:12px;justify-content:space-between;padding:0 12px}
.profile-link{gap:8px;padding:6px 10px;border-radius:6px}
.profile-link:hover{background:#f4f6f8}
.username{margin-left:6px;font-weight:600;color:#333}

/* Positioning for icons: ensure natural order and spacing with sensible z-index */
.home-link{z-index:3;position:relative;margin-left:8px}
.report-link,.calendar-link{z-index:2}
.profile-link{z-index:6;position:relative;margin-right:-12px}

.profile-wrapper{position:relative;margin-left:12px;transform:translateX(-30px);transition:transform 180ms ease}
.report-link,.calendar-link{gap:8px;padding:6px 10px;border-radius:6px;display:inline-flex;align-items:center}
.report-link:hover,.calendar-link:hover{background:#f4f6f8}
/* Hide labels visually by default; reveal with smooth fade+slide on hover */
.report-text,
.home-text,
.calendar-text {
  order: -1; /* render label before icon */
  margin-right: 8px;
  font-weight:600;
  color:#0f172a;
  background: transparent;
  padding: 0 0;
  white-space: nowrap;
  max-width: 0; /* collapsed by default */
  opacity: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: max-width 200ms ease, opacity 160ms ease, padding 140ms ease, background 140ms ease;
}
.icon-link:hover .report-text,
.icon-link:focus .report-text,
.icon-link:hover .home-text,
.icon-link:focus .home-text,
.icon-link:hover .calendar-text,
.icon-link:focus .calendar-text {
  max-width: 160px; /* expand to reveal text */
  opacity: 1;
  padding: 6px 8px;
  background: rgba(15,23,42,0.06);
  border-radius: 6px;
}

/* Responsive rules: adjust header for small screens */
  @media (max-width: 720px) {
  header { padding: 10px; }
  .brand-flag { height: 20px; margin-right:8px }
  .icon-nav{margin-left:8px}
  /* On small screens remove the left shift so icons stay visible */
  .icon-nav{transform:translateX(0) !important}
  .profile-wrapper{transform:translateX(0) !important}
  /* Always hide label text on small screens and rely on icons */
  .report-text, .home-text, .calendar-text { opacity: 0 !important; transform: translateY(6px) scale(0.98) !important; pointer-events: none !important }
  /* Reduce spacing and make icons tighter */
  .icon-link{padding:6px 8px}
  .nav-actions{gap:6px;max-width:60%;transform:translateX(-16px)}
}

@media (min-width: 721px) and (max-width: 1000px) {
  /* Slightly reduce gap on medium screens */
  .icon-nav{gap:6px}
}
.profile-menu{position:absolute;right:0;top:46px;background:#fff;border-radius:8px;box-shadow:0 8px 24px rgba(15,23,42,0.12);min-width:200px;overflow:hidden}
.profile-menu .menu-item{display:block;padding:10px 14px;color:#333;text-decoration:none;border-bottom:1px solid #f0f0f0;background:#fff;text-align:left}
.profile-menu .menu-item:hover{background:#f7f9fb}
.profile-menu .logout{width:100%;border:none;background:#fff;cursor:pointer}
.profile-menu .menu-item.logout{color:#c0392b}

</style>

