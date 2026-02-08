<template>
  <!-- Lista principal de operativos: muestra tablas y modal de detalles -->
  <div class="operativos-container">
    <h1>Lista de Operativos</h1>

    <div class="operativos-card">
      <div class="card-header">Seleccione un Operativo</div>
      <div class="card-body">

    <!-- Mensaje de notificación breve (success/error) -->
    <div v-if="notification.message" :class="['notification', notification.type]">
      {{ notification.message }}
    </div>

    <div v-if="loading">Cargando...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <!-- Lista de operativos (fila por fila) -->
    <div v-if="operativos.length" class="operativos-list">
      <div class="list-row" v-for="operativo in operativos" :key="operativo.id" @click="$router.push({ name: 'VerificarTrabajador', params: { id: operativo.id } })">
        <div class="row-left">
          <div class="operativo-main">
            <div class="operativo-title">{{ operativo.titulo }}</div>
            <div class="subtitle">{{ formatDate(operativo.fecha_inicio) }} • {{ operativo.tipo_operativo || '' }}</div>
          </div>
        </div>
        <div class="row-right">
          <div class="lugar">{{ operativo.lugar }}</div>
          <div class="acciones">
            <button @click.stop="showDetails(operativo)" class="details-button">Ver Detalles</button>
          </div>
        </div>
      </div>
    </div>
      </div>
    </div>
    <p v-if="!loading && !operativos.length">No se encontraron operativos.</p>

    <!-- Modal para mostrar detalles del operativo seleccionado -->
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
          <li><strong>Estatus:</strong> {{ selectedOperativo.estatus }}</li>
          <li><strong>Lugar:</strong> {{ selectedOperativo.lugar }}</li>
          <li><strong>Tipo de Operativo:</strong> {{ selectedOperativo.tipo_operativo }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
// Componente que obtiene la lista de operativos desde `/api/libro/` y muestra detalles
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
    // Petición GET para cargar operativos al montar el componente
    fetchOperativos() {
      this.loading = true;
      this.error = null;
      axios.get('/api/libro/')
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
      // Abre el modal con los datos del operativo seleccionado
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
      // Mostrar notificación breve en la parte superior
      this.notification.message = message;
      this.notification.type = type;
      setTimeout(() => {
        this.notification.message = '';
      }, 3000);
    }
  },
  mounted() {
    this.fetchOperativos(); // Cargar datos al montar
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

/* Card layout */
.operativos-card{background: rgba(255,255,255,0.95);border-radius:6px;box-shadow:0 6px 18px rgba(15,23,42,0.06);overflow:hidden}
.card-header{padding:14px 18px;font-weight:700;background:transparent;color:#333;border-bottom:1px solid #eee}
.card-body{padding:0}

/* Table styled as list rows */
/* List rows layout */
.operativos-list{display:block}
.list-row{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border-bottom:1px solid #f0f0f0;background:#fff}
.list-row + .list-row{border-top:0}
.list-row{cursor:pointer}
.list-row:hover{background:#fbfbfb}
.row-left{flex:1}
.operativo-main{display:flex;flex-direction:column}
.operativo-title{font-weight:600;color:#333}
.operativo-title a{color:inherit;text-decoration:none}
.operativo-title a:hover{text-decoration:underline}
.subtitle{font-size:0.9rem;color:#777;margin-top:6px}
.row-right{display:flex;gap:16px;align-items:center}
.lugar{color:#666;min-width:220px;text-align:right}
.acciones{min-width:140px;text-align:right}

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

/* Responsive: make list rows stack and allow content to wrap */
@media (max-width: 720px) {
  .operativos-container { padding: 12px }
  .operativos-card { border-radius:6px }
  .list-row { flex-direction: column; align-items: flex-start; gap:8px; padding:12px }
  .row-right { width:100%; display:flex; justify-content:space-between; gap:8px }
  .lugar { text-align:left; min-width: auto }
  .acciones { text-align:left; min-width: auto }
  .subtitle { font-size:0.85rem }
}

@media (max-width: 420px) {
  .operativo-title{font-size:1rem}
  .subtitle{font-size:0.8rem}
}
</style>
