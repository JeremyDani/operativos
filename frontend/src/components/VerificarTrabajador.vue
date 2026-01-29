<template>
  <div class="verificar-container">
    <h1>Verificar Trabajador</h1>
    <div class="verificar-form">
      <input type="text" v-model="cedula" placeholder="Ingrese la cédula del trabajador" @keyup.enter="verificarCedula"/>
      <button @click="verificarCedula">Verificar</button>
    </div>
    <div v-if="loading">Cargando...</div>
    <div v-if="mensaje" class="mensaje" :class="mensajeTipo">{{ mensaje }}</div>
    <div v-if="resultado" class="resultado-panel">
      <h3>Resultado para la Cédula: {{ resultado.cedula }}</h3>
      <p><strong>Nombres:</strong> {{ resultado.nombres }}</p>
      <p><strong>Apellidos:</strong> {{ resultado.apellidos }}</p>
      <p><strong>Cargo:</strong> {{ resultado.cargo }}</p>
      <p><strong>Dependencia:</strong> {{ resultado.dependencia }}</p>
    </div>

    <!-- Modal: muestra datos del operativo y datos de la nómina -->
    <div v-if="modalVisible" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2>Confirmar Participación</h2>
        <div class="modal-section">
          <h3>Operativo</h3>
          <p><strong>Título:</strong> {{ operativo.titulo }}</p>
          <p><strong>Lugar:</strong> {{ operativo.lugar }}</p>
          <p><strong>Estatus:</strong> {{ operativo.estatus }}</p>
          <p><strong>Fecha inicio:</strong> {{ formatoFecha(operativo.fecha_inicio) }}</p>
        </div>
        <div class="modal-section">
          <h3>Trabajador (Nómina)</h3>
          <p><strong>Cédula:</strong> {{ trabajador.cedula }}</p>
          <p><strong>Nombre:</strong> {{ trabajador.nombres }}</p>
          <p><strong>Apellidos:</strong> {{ trabajador.apellidos || '-' }}</p>
          <p><strong>Cargo:</strong> {{ trabajador.cargo || '-' }}</p>
          <p><strong>Ente:</strong> {{ trabajador.ente || '-' }}</p>
        </div>
        <div class="modal-actions">
          <button class="btn-continue" @click="confirmarParticipacion">Continuar</button>
          <button class="btn-cancel" @click="closeModal">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VerificarTrabajador',
  data() {
    return {
      cedula: '',
      loading: false,
      mensaje: '',
      mensajeTipo: '', // 'success', 'error', 'info'
      resultado: null,
      modalVisible: false,
      operativo: {},
      trabajador: {}
    };
  },
  methods: {
    verificarCedula() {
      if (!this.cedula) {
        this.mensaje = 'Por favor, ingrese una cédula.';
        this.mensajeTipo = 'error';
        this.resultado = null;
        return;
      }
      this.loading = true;
      this.mensaje = '';
      this.resultado = null;
      const operativoId = this.$route.params.id;

      axios.get(`http://localhost:8000/api/operativos/${operativoId}/verificar/${this.cedula}`)
        .then(response => {
          const data = response.data;
          if (data.encontrado) {
            this.trabajador = data.trabajador || {};
            // fetch operativo details
            return axios.get(`http://localhost:8000/api/libro/${operativoId}`)
              .then(r => {
                this.operativo = r.data;
                this.modalVisible = true;
                this.mensaje = 'Trabajador encontrado. Confirme para registrar.';
                this.mensajeTipo = 'info';
              });
          } else {
            this.mensaje = data.message || 'Trabajador no encontrado.';
            this.mensajeTipo = 'error';
          }
        })
        .catch(error => {
          if (error.response) {
            this.mensaje = error.response.data.detail || 'Error al verificar la cédula.';
            this.mensajeTipo = 'error';
          } else {
            this.mensaje = 'Error de conexión con el servidor.';
            this.mensajeTipo = 'error';
          }
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    confirmarParticipacion() {
      const operativoId = this.$route.params.id;
      const payload = {
        cedula: String(this.trabajador.cedula || this.cedula),
        nombres: this.trabajador.nombres || '',
        apellidos: this.trabajador.apellidos || '',
        cargo: this.trabajador.cargo || '',
        ente: this.trabajador.ente || ''
      };
      this.loading = true;
      axios.post(`http://localhost:8000/api/operativos/${operativoId}/guardar-participacion`, payload)
        .then(response => {
          this.mensaje = response.data.message || 'Participación registrada.';
          this.mensajeTipo = 'success';
          this.modalVisible = false;
          this.resultado = this.trabajador;
        })
        .catch(error => {
          this.mensaje = (error.response && error.response.data && (error.response.data.message || error.response.data.detail)) || 'Error al guardar la participación.';
          this.mensajeTipo = 'error';
        })
        .finally(() => {
          this.loading = false;
        });
    },
    closeModal() {
      this.modalVisible = false;
    },
    formatoFecha(dateString) {
      if (!dateString) return '-';
      return new Date(dateString).toLocaleString();
    }
  }
};
</script>

<style scoped>
.verificar-container {
  width: 80%;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.verificar-form {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
.verificar-form input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.verificar-form button {
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.verificar-form button:hover {
  background-color: #218838;
}
.resultado-panel {
  margin-top: 20px;
  padding: 15px;
  background-color: #e9ecef;
  border-left: 5px solid #007bff;
}
.mensaje {
  padding: 10px;
  margin-top: 20px;
  border-radius: 5px;
  color: #fff;
}
.mensaje.success {
  background-color: #28a745;
}
.mensaje.error {
  background-color: #dc3545;
}
.mensaje.info {
  background-color: #17a2b8;
}

/* Modal styles */
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
  z-index: 1000;
}
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 6px;
  max-width: 600px;
  width: 90%;
}
.modal-section { margin-bottom: 12px; }
.modal-actions { display:flex; gap:10px; justify-content:flex-end; }
.btn-continue { background:#007bff; color:#fff; padding:8px 14px; border:none; border-radius:4px; cursor:pointer }
.btn-cancel { background:#6c757d; color:#fff; padding:8px 14px; border:none; border-radius:4px; cursor:pointer }
</style>
