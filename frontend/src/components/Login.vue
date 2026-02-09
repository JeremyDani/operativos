<template>
  <!-- Contenedor de login: formulario controla `username` y `password` -->
  <div class="login-page">
    <div class="login-left">
      <div class="login-card">
        <picture class="brand-small">
          <img :src="logoSmall" alt="SGI-Operativos" />
        </picture>
        <h2 class="title">SGI-Operativos</h2>
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

    <div class="login-right" :style="{ backgroundImage: `url(${fondo})` }">
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
        const userId = Object.prototype.hasOwnProperty.call(userPayload, 'id')
          ? userPayload.id
          : null;
        const username = userPayload.username || this.username || '';
        const nombreApellido = userPayload.nombre_apellido
          || (userPayload.first_name
                ? `${userPayload.first_name} ${userPayload.last_name || ''}`.trim()
                : '');
        const nombre = nombreApellido || username;
        const email = userPayload.email || '';
        const origen = userPayload.origen || '';
        const cedula = Object.prototype.hasOwnProperty.call(userPayload, 'cedula')
          ? userPayload.cedula
          : null;

        // Normalizar roles: el backend puede devolver nombres (strings) o grupos (objetos)
        let roles = [];
        if (Array.isArray(userPayload.roles) && userPayload.roles.length) {
          roles = userPayload.roles.map(r => (typeof r === 'string' ? r : (r.name || r.nombre || ''))).filter(Boolean);
        } else if (Array.isArray(userPayload.groups) && userPayload.groups.length) {
          roles = userPayload.groups.map(g => (typeof g === 'string' ? g : (g.name || g.nombre || ''))).filter(Boolean);
        }

        auth.setUser({ id: userId, nombre, nombre_apellido: nombreApellido, username, email, origen, cedula, roles });
        console.debug('Login: auth.setUser llamado', { userId, nombre, nombreApellido, username, email, origen, cedula, roles }, auth.isAuthenticated, auth.user);

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
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.38fr);
  gap: 0;
  width: 100vw;
  padding: 0;
  margin: 0;
  background-color: #ffffff;
}
.login-left{flex:1;max-width:none;display:flex;justify-content:center;align-items:center;padding:2rem 4rem}
.login-card{background:#ffffff;padding:2.5rem 3rem;border-radius:16px;box-shadow:0 18px 45px rgba(15,23,42,0.10);max-width:420px;width:100%;text-align:left}
.brand-small img{max-width:220px;display:block;margin:0 0 1rem 0}
.title{margin:0 0 1.5rem 0;color:#111;font-size:1.6rem;font-weight:700}
.login-form .form-group{margin-bottom:1rem}
.login-form label{display:block;margin-bottom:0.4rem;color:#444}
.login-form input{width:100%;padding:0.75rem;border:1px solid #e6e9ee;border-radius:6px}
.btn-primary{width:100%;padding:0.85rem;background:#0d6efd;color:#fff;border:none;border-radius:999px;cursor:pointer;box-shadow:0 10px 24px rgba(13,110,253,0.25);font-weight:600}
.btn-primary:active{transform:translateY(1px)}
.error-message{color:#c92a2a;margin-top:1rem}
.login-right{flex:0 0 38%;height:100vh;display:flex;align-items:flex-end;justify-content:flex-end;background-size:cover;background-position:center;border-radius:0;overflow:hidden}
.right-brand{display:flex;align-items:center;gap:1.5rem;padding:1.5rem 1.8rem;background:rgba(0,0,0,0.4);border-radius:0;margin:0}
.right-logo{max-width:260px;filter:drop-shadow(0 6px 18px rgba(0,0,0,0.45))}
.right-text h3{margin:0;font-size:1.4rem}
.right-text p{margin:0;color:#555}
@media (max-width:900px){
  .login-page{flex-direction:column}
  .login-left{flex:0 0 auto;padding:1.5rem}
  .login-right{flex:0 0 auto;width:100%;height:260px}
}

@media (max-width:720px){
  .login-left{padding:1.25rem}
  .login-right{height:220px}
  .brand-small img{max-width:160px}
}
</style>
