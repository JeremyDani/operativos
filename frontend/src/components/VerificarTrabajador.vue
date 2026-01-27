<template>
  <div class="verificar-container">
    <h1>Verificar Trabajador en Operativo</h1>
    <div v-if="operativo">
      <h2>{{ operativo.titulo }}</h2>
      <p><strong>Lugar:</strong> {{ operativo.lugar }}</p>
      <p><strong>Estatus:</strong> {{ operativo.estatus }}</p>
    </div>
    <div class="verificar-form">
      <input type="text" v-model="cedula" placeholder="Ingrese la cédula del trabajador" />
      <button @click="verificarTrabajador">Verificar</button>
    </div>
    <div v-if="resultado" class="resultado-panel">
      <h3>Resultado:</h3>
      <p>{{ resultado }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      operativo: null, // Aquí guardaremos los detalles del operativo
      cedula: '',
      resultado: ''
    };
  },
  methods: {
    fetchOperativoDetails() {
      // Lógica para buscar los detalles del operativo usando el ID de la URL
      // Por ahora, lo dejamos como un placeholder
      const operativoId = this.$route.params.id;
      console.log("Buscando detalles para el operativo ID:", operativoId);
      // Simulación:
      this.operativo = { 
        titulo: `Operativo #${operativoId}`, 
        lugar: 'Lugar de Prueba', 
        estatus: 'Activo' 
      };
    },
    verificarTrabajador() {
      if (!this.cedula) {
        this.resultado = 'Por favor, ingrese una cédula.';
        return;
      }
      // Lógica para llamar al backend y verificar la cédula en este operativo
      console.log(`Verificando cédula ${this.cedula} en operativo ${this.$route.params.id}`);
      // Simulación de respuesta:
      this.resultado = `El trabajador con cédula ${this.cedula} SÍ pasó por el operativo.`;
      // En caso de no encontrarlo:
      // this.resultado = `El trabajador con cédula ${this.cedula} NO se encontró en este operativo.`;
    }
  },
  mounted() {
    this.fetchOperativoDetails();
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
</style>
