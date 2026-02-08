<template>
  <!-- Contenedor de login: formulario controla `username` y `password` -->
  <div class="login-page" :style="{ backgroundImage: `url(${fondo})` }">
    <div class="login-left">
      <div class="login-card">
        <picture class="brand-small">
          <img :src="logoSmall" alt="SGI-Operativos" />
        </picture>
        <h2 class="title">Por favor ingrese sus credenciales</h2>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">Usuario</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div class="form-group">
            <label for="password">Clave</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <button type="submit" class="btn-primary">Ingresar</button>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>

    <div class="login-right">
      <div class="right-brand">
      <img :src="logoMppe" alt="Gobierno Bolivariano" class="right-logo" />
        <div class="right-text">
          <h3>Gobierno Bolivariano de Venezuela</h3>
          <p>Ministerio del Poder Popular para la Educación</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Manejo del login: envía credenciales al endpoint de Django y actualiza `authState`
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

export default {
  data() {
    return {
      username: '',
      password: '',
      // Mensajes de feedback para el usuario
      errorMessage: '',
      successMessage: ''
      ,
      // URLs a assets públicos (Vite sirve `frontend/public` en la raíz durante desarrollo)
      logoSmall: new URL('/logoprueba.png', import.meta.url).href,
      logoMppe: new URL('/logomppe.png', import.meta.url).href,
      fondo: new URL('/fondo.jpg', import.meta.url).href
    };
  },
  methods: {
    async handleLogin() {
      // Reset de mensajes
      this.errorMessage = '';
      this.successMessage = '';
      try {
          console.debug('Login: intentando iniciar sesión', this.username);
        // Petición POST al endpoint de autenticación del backend
        const response = await axios.post('/api/cuenta/login/', {
          username: this.username,
          password: this.password,
        });

        // Backend devuelve un mensaje y datos del usuario; marcar al usuario como autenticado
        this.successMessage = response.data.message;
        const auth = useAuthStore();

        // Extraer payload del usuario y propagar roles al store
        const userPayload = response.data.user || response.data || {};
        const nombre = userPayload.first_name
          ? `${userPayload.first_name} ${userPayload.last_name || ''}`.trim()
          : (userPayload.username || this.username || '');
        const email = userPayload.email || '';

        // Normalizar roles: el backend puede devolver nombres (strings) o grupos (objetos)
        let roles = [];
        if (Array.isArray(userPayload.roles) && userPayload.roles.length) {
          roles = userPayload.roles.map(r => (typeof r === 'string' ? r : (r.name || r.nombre || ''))).filter(Boolean);
        } else if (Array.isArray(userPayload.groups) && userPayload.groups.length) {
          roles = userPayload.groups.map(g => (typeof g === 'string' ? g : (g.name || g.nombre || ''))).filter(Boolean);
        }

        auth.setUser({ nombre, email, roles });
        console.debug('Login: auth.setUser llamado', { nombre, email, roles }, auth.isAuthenticated, auth.user);

        this.$router.push('/operativos'); // redirigir a la lista de operativos
        // Nota: aquí se podría guardar un token en localStorage si el backend lo devuelve

      } catch (error) {
        // Manejo de errores: distinguir entre respuesta del servidor y fallo de conexión
        if (error.response) {
          this.errorMessage = error.response.data.error || 'Error en el servidor.';
        } else if (error.request) {
          this.errorMessage = 'No se pudo conectar con el servidor. ¿Está funcionando?';
        } else {
          this.errorMessage = 'Error al crear la solicitud de inicio de sesión.';
        }
        console.error('Error de login:', error);
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  min-height: 70vh;
  display: flex;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-image: url('/fondo.jpg');
  background-size: cover;
  background-position: center;
}
.login-left{flex:0 0 44%;max-width:640px}
.login-card{background: rgba(255,255,255,0.95);padding:2rem;border-radius:8px;box-shadow:0 8px 30px rgba(15,23,42,0.08)}
.brand-small img{max-width:220px;display:block;margin:0 0 1rem 0}
.title{margin:0 0 1rem 0;color:#222}
.login-form .form-group{margin-bottom:1rem}
.login-form label{display:block;margin-bottom:0.4rem;color:#444}
.login-form input{width:100%;padding:0.75rem;border:1px solid #e6e9ee;border-radius:6px}
.btn-primary{width:100%;padding:0.75rem;background:#0d6efd;color:#fff;border:none;border-radius:6px;cursor:pointer;box-shadow:0 6px 18px rgba(13,110,253,0.14)}
.btn-primary:active{transform:translateY(1px)}
.error-message{color:#c92a2a;margin-top:1rem}
.login-right{flex:1 1 46%;display:flex;align-items:center;justify-content:center}
.right-brand{display:flex;align-items:center;gap:1.5rem;padding:2rem;background:rgba(255,255,255,0.6);border-radius:8px}
.right-logo{max-width:320px}
.right-text h3{margin:0;font-size:1.4rem}
.right-text p{margin:0;color:#555}
@media (max-width:900px){.login-page{flex-direction:column}.login-left,.login-right{max-width:720px}}

@media (max-width:720px){
  .login-page{padding:1rem}
  .login-left{flex:1 1 100%;max-width:100%}
  .login-right{flex:1 1 100%;max-width:100%;margin-top:12px}
  .brand-small img{max-width:160px}
  .right-text h3{font-size:1rem}
  .right-text p{font-size:0.9rem}
}
</style>
