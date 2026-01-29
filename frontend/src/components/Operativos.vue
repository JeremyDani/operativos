<template>
  <div class="operativos-container">
    <h1>Lista de Operativos</h1>

    <!-- Notificación -->
    <div v-if="notification.message" :class="['notification', notification.type]">
      {{ notification.message }}
    </div>

    <div v-if="loading">Cargando...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <table v-if="operativos.length">
      <thead>
        <tr>
          <th>Operativos</th>
          <th>Lugar</th>
          <th>Estatus</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="operativo in operativos" :key="operativo.id">
          <td>
            <router-link :to="{ name: 'VerificarTrabajador', params: { id: operativo.id } }">
              {{ operativo.titulo }}
            </router-link>
          </td>
          <td>{{ operativo.lugar }}</td>
          <td>{{ operativo.estatus }}</td>
          <td>
            <button @click="showDetails(operativo)" class="details-button">
              Ver Detalles
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="!loading">No se encontraron operativos.</p>

    <!-- Modal para mostrar detalles -->
    <div v-if="selectedOperativo" class="modal-overlay" @click="closeDetails">
      <div class="modal-content" @click.stop>
        <span class="close-button" @click="closeDetails">&times;</span>
        <h2>Detalles del Operativo</h2>
        <ul>
          <li><strong>Título:</strong> {{ selectedOperativo.titulo }}</li>
          <li><strong>Descripción:</strong> {{ selectedOperativo.descripcion }}</li>
          <li><strong>Fecha de Inicio:</strong> {{ formatDate(selectedOperativo.fecha_inicio) }}</li>
          <li><strong>Fecha de Fin:</strong> {{ formatDate(selectedOperativo.fecha_fin) }}</li>
          <li><strong>Motivo:</strong> {{ selectedOperativo.motivo }}</li>
          <li><strong>Publicado:</strong> {{ selectedOperativo.publicado ? 'Sí' : 'No' }}</li>
          <li><strong>Ilustración:</strong> {{ selectedOperativo.ilustracion }}</li>
          <li><strong>Estatus:</strong> {{ selectedOperativo.estatus }}</li>
          <li><strong>Lugar:</strong> {{ selectedOperativo.lugar }}</li>
          <li><strong>Tipo de Operativo:</strong> {{ selectedOperativo.tipo_operativo }}</li>
          <li><strong>Usa Telegram:</strong> {{ selectedOperativo.usar_telegram ? 'Sí' : 'No' }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      operativos: [],
      loading: true,
      error: null,
      selectedOperativo: null,
      notification: {
        message: '',
        type: '' // 'success' o 'error'
      }
    };
  },
  methods: {
    fetchOperativos() {
      this.loading = true;
      this.error = null;
      axios.get('http://localhost:8000/api/libro/')
        .then(response => {
          this.operativos = response.data;
        })
        .catch(error => {
          console.error('Error al obtener operativos:', error);
          this.error = 'No se pudo conectar con el servidor o no se encontraron datos.';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    showDetails(operativo) {
      this.selectedOperativo = operativo;
    },
    closeDetails() {
      this.selectedOperativo = null;
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    showNotification(message, type) {
      this.notification.message = message;
      this.notification.type = type;
      setTimeout(() => {
        this.notification.message = '';
      }, 3000);
    }
  },
  mounted() {
    this.fetchOperativos();
  }
};
</script>

<style scoped>
.operativos-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.notification {
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 5px;
  text-align: center;
}

.notification.success {
  background-color: #d4edda;
  color: #155724;
}

.notification.error {
  background-color: #f8d7da;
  color: #721c24;
}

.error-message {
  color: red;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.details-button, .register-button {
  padding: 5px 10px;
  cursor: pointer;
  border: none;
  border-radius: 3px;
}

.details-button {
  background-color: #007bff;
  color: white;
}

.register-button {
  background-color: #28a745;
  color: white;
}

.registro-form {
  display: flex;
  gap: 5px;
}

.registro-form input {
  padding: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  max-width: 500px;
  width: 100%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
}

.modal-content li {
  margin-bottom: 10px;
}
</style>
