<template>
  <div class="operativos-container">
    <h1>Lista de Operativos</h1>
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
      selectedOperativo: null, // Para guardar el operativo seleccionado
    };
  },
  methods: {
    fetchOperativos() {
      this.loading = true;
      this.error = null;
      axios.get('http://localhost:8000/libro/')
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
    // Método para mostrar el modal con los detalles
    showDetails(operativo) {
      this.selectedOperativo = operativo;
    },
    // Método para cerrar el modal
    closeDetails() {
      this.selectedOperativo = null;
    },
    // Método para formatear la fecha
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    }
  },
  mounted() {
    this.fetchOperativos();
  }
};
</script>

<style scoped>
.operativos-container {
  width: 80%;
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
th {
  background-color: #f4f4f4;
}
.error-message {
  color: red;
}
.details-button {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.details-button:hover {
  background-color: #0056b3;
}

/* Estilos para el Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  position: relative;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.modal-content ul {
  list-style-type: none;
  padding: 0;
}
.modal-content li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}
.modal-content li:last-child {
  border-bottom: none;
}
.close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
}
</style>
