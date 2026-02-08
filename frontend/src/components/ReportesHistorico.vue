<template>
  <!-- Página de reportes: carga estadísticas históricas y dibuja charts -->
  <div class="reportes-container">
    <h2>Reporte: Participaciones históricas</h2>
    <div class="stats">
      <section class="stat-block">
        <h3>Empleados por Ente</h3>
        <ul>
          <li v-for="row in porEnte" :key="row.ente">{{ row.ente }}: {{ row.count }}</li>
        </ul>
      </section>
      <section class="stat-block">
        <h3>Por Tipo de Operativo</h3>
        <ul>
          <li v-for="row in porTipo" :key="row.tipo">{{ row.tipo }}: {{ row.count }}</li>
        </ul>
      </section>
    </div>

    <div class="charts">
      <!-- Canvas donde Chart.js renderiza las gráficas -->
      <canvas id="chart-ente"></canvas>
      <canvas id="chart-tipo"></canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  name: 'ReportesHistorico',
  data() {
    return {
      porEnte: [],
      porTipo: []
    };
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      // Llamada al endpoint que devuelve estadísticas agregadas del histórico
      // Se usa URL completa para evitar issues con proxy en entorno Vite
      const res = await axios.get('http://127.0.0.1:8000/api/historico/stats');
      this.porEnte = res.data.por_ente || [];
      this.porTipo = res.data.por_tipo_operativo || [];
      this.renderCharts();
    },
    renderCharts() {
      const ctx1 = document.getElementById('chart-ente').getContext('2d');
      new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: this.porEnte.map(r => r.ente),
          datasets: [{ label: 'Empleados', data: this.porEnte.map(r => r.count), backgroundColor: '#42b983' }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });

      const ctx2 = document.getElementById('chart-tipo').getContext('2d');
      new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: this.porTipo.map(r => r.tipo),
          datasets: [{ label: 'Participaciones', data: this.porTipo.map(r => r.count), backgroundColor: '#369f71' }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }
  }
};
</script>

<style scoped>
.reportes-container { width: 90%; max-width: 1000px; margin: 20px auto; }
.stats { display:flex; gap:20px; justify-content:space-between; }
.stat-block { flex:1; background:#fff; padding:12px; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.08); }
.charts { display:flex; gap:20px; margin-top:20px; }
canvas { flex:1; height:300px; background:#fff; border-radius:6px; padding:8px; }
</style>
