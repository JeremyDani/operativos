<template>
  <div class="login-container">
    <h2>Login de Usuario</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Usuario:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Iniciar Sesión</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { authState } from '../auth';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = '';
      this.successMessage = '';
      try {
        const response = await axios.post('http://localhost:8000/api/cuenta/login/', {
          username: this.username,
          password: this.password,
        });
        
        this.successMessage = response.data.message;
        alert(response.data.message); // Muestra un popup de éxito
        authState.isAuthenticated = true;
        this.$router.push('/operativos');
        // Aquí podrías redirigir al usuario o guardar el token de sesión
        
      } catch (error) {
        if (error.response) {
          // El servidor respondió con un código de estado fuera del rango 2xx
          this.errorMessage = error.response.data.error || 'Error en el servidor.';
        } else if (error.request) {
          // La solicitud se hizo pero no se recibió respuesta
          this.errorMessage = 'No se pudo conectar con el servidor. ¿Está funcionando?';
        } else {
          // Algo sucedió al configurar la solicitud
          this.errorMessage = 'Error al crear la solicitud de inicio de sesión.';
        }
        console.error('Error de login:', error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #369f71;
}
.error-message {
  color: red;
  margin-top: 15px;
}
</style>
