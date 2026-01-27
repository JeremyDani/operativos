<template>
  <div class="operativos-container">
    <h1>Lista de Operativos</h1>
    <div v-if="loading">Cargando...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <table v-if="operativos.length">
      <thead>
        <tr>
          <th>Título del Operativo</th>
          <th>Estatus del Operativo</th>
          <!-- Agrega más columnas según los datos de tu modelo -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="operativo in operativos" :key="operativo.id">
          <td>{{ operativo.nombre }}</td>
          <td>{{ operativo.estatus }}</td>
          <!-- Agrega más celdas según los datos -->
        </tr>
      </tbody>
    </table>
    <p v-else-if="!loading">No se encontraron operativos.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      operativos: [],
      loading: true,
      error: null
    };
  },
  methods: {
    async fetchOperativos() {
      this.loading = true;
      this.error = null;
      try {
        // NOTA: La URL '/api/operativos/' es un ejemplo.
        // Necesitamos verificar cuál es la URL correcta en tu API de Django.
        const response = await axios.get('http://localhost:8000/api/libro/'); // <-- REVISAR ESTA URL
        this.operativos = response.data; 
      } catch (err) {
        this.error = 'Error al cargar los operativos. Por favor, intenta de nuevo más tarde.';
        console.error(err);
      } finally {
        this.loading = false;
      }
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
</style>
