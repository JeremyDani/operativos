<template>
  <!-- Dashboard de reportes históricos estilo panel de analítica -->
  <div class="reportes-dashboard">
    <!-- Sidebar simple inspirada en el diseño de ejemplo -->
    <aside class="sidebar">
    </aside>

    <!-- Contenido principal -->
    <div class="dashboard-main">
      <!-- Barra superior: título, pestañas y filtros rápidos -->
      <header class="topbar">
        <div class="topbar-left">
          <h1>Reporte</h1>
          <div class="topbar-subtitle">Reporte  de participaciones en los operativos</div>
          <div class="topbar-subtitle" v-if="startDate && endDate">
            Desde {{ formatDate(startDate) }} hasta {{ formatDate(endDate) }}
          </div>
        </div>
        <div class="topbar-right">
          <div class="date-filters">
            <input
              type="date"
              class="date-input"
              v-model="startDate"
              @change="onDateChange"
            />
            <span class="date-separator">—</span>
            <input
              type="date"
              class="date-input"
              v-model="endDate"
              @change="onDateChange"
            />
          </div>
          <button class="btn-download" @click="downloadPdf">
            Descargar PDF
          </button>
        </div>
      </header>

      <!-- Tarjetas de KPIs principales -->
      <section class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-label">Total participaciones</div>
          <div class="kpi-value">{{ totalParticipaciones }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Entes con registros</div>
          <div class="kpi-value">{{ porEnte.length }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Tipos de operativo</div>
          <div class="kpi-value">{{ porTipo.length }}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Promedio por ente</div>
          <div class="kpi-value">{{ promedioPorEnte }}</div>
        </div>
      </section>

      <!-- Zona principal de gráficas y listados -->
      <section class="main-grid">
        <!-- Gráfica grande: participaciones por ente -->
        <div class="card card-large">
          <div class="card-header">
            <div>
              <div class="card-title">Participaciones por ente</div>
              <div class="card-subtitle">Distribución de registros históricos</div>
            </div>
            <div class="card-tabs">
              <button class="tab active">Barra</button>
              <button class="tab" disabled>Línea</button>
            </div>
          </div>
          <div class="card-body chart-wrapper">
            <canvas id="chart-ente"></canvas>
          </div>
        </div>

        <!-- Gráfica lateral: por tipo de operativo -->
        <div class="card card-side">
          <div class="card-header">
            <div class="card-title">Por tipo de operativo</div>
          </div>
          <div class="card-body chart-wrapper">
            <canvas id="chart-tipo"></canvas>
          </div>
        </div>
      </section>

      <!-- Listados de detalle inferiores -->
      <section class="bottom-grid">
        <div class="card">
          <div class="card-header">
            <div class="card-title">Top entes por participación</div>
          </div>
          <div class="card-body list-body">
            <div v-if="!porEnte.length" class="empty-text">Sin datos de entes.</div>
            <ul v-else>
              <li v-for="row in topEnte" :key="row.ente" class="list-row">
                <span class="list-name">{{ row.ente }}</span>
                <span class="list-badge">{{ row.count }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">Participaciones por tipo</div>
          </div>
          <div class="card-body list-body">
            <div v-if="!porTipo.length" class="empty-text">Sin datos de tipos.</div>
            <ul v-else>
              <li v-for="row in porTipo" :key="row.tipo" class="list-row">
                <span class="list-name">{{ row.tipo }}</span>
                <span class="list-badge badge-secondary">{{ row.count }}</span>
              </li>
            </ul>
          </div>
        </div>
      </section>
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
      porTipo: [],
      // Filtros de fecha (día/mes/año) para acotar el histórico
      startDate: '',
      endDate: '',
      // Referencias a las instancias de Chart para poder actualizarlas
      chartEnte: null,
      chartTipo: null
    };
  },
  computed: {
    totalParticipaciones() {
      const totalEnte = this.porEnte.reduce((acc, r) => acc + (r.count || 0), 0);
      const totalTipo = this.porTipo.reduce((acc, r) => acc + (r.count || 0), 0);
      // Preferir el total por tipo si existe, si no usar por ente
      return totalTipo || totalEnte || 0;
    },
    promedioPorEnte() {
      if (!this.porEnte.length) return 0;
      const total = this.porEnte.reduce((acc, r) => acc + (r.count || 0), 0);
      return (total / this.porEnte.length).toFixed(1);
    },
    topEnte() {
      // Ordenar de mayor a menor y mostrar solo algunos
      return [...this.porEnte]
        .sort((a, b) => (b.count || 0) - (a.count || 0))
        .slice(0, 6);
    }
  },
  mounted() {
    // Inicializar los filtros en la fecha actual (YYYY-MM-DD)
    const hoy = new Date().toISOString().slice(0, 10);
    this.startDate = hoy;
    this.endDate = hoy;
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      // Llamada al endpoint que devuelve estadísticas agregadas del histórico
      // Se usa URL completa para evitar issues con proxy en entorno Vite
      const params = {};
      if (this.startDate) params.desde = this.startDate;
      if (this.endDate) params.hasta = this.endDate;

      // Usar ruta relativa para que pase por el mismo origen
      // (Vite proxy hacia Django) y evitar problemas de CORS.
      const res = await axios.get('/api/historico/stats', { params });
      this.porEnte = res.data.por_ente || [];
      this.porTipo = res.data.por_tipo_operativo || [];
      this.renderCharts();
    },
    onDateChange() {
      // Cada vez que cambie alguno de los filtros de fecha
      // se vuelve a consultar la API con el nuevo rango.
      this.fetchStats();
    },
    formatDate(isoDate) {
      if (!isoDate) return '';
      const [year, month, day] = isoDate.split('-');
      if (!year || !month || !day) return isoDate;
      // Mostrar como día/mes/año
      return `${day}/${month}/${year}`;
    },
    downloadPdf() {
      // Usar la función de impresión del navegador para generar un PDF
      // tipo "captura" de la página (escogiendo "Guardar como PDF").
      window.print();
    },
    renderCharts() {
      const canvasEnte = document.getElementById('chart-ente');
      const canvasTipo = document.getElementById('chart-tipo');

      if (!canvasEnte || !canvasTipo) return;

      const ctx1 = canvasEnte.getContext('2d');
      const ctx2 = canvasTipo.getContext('2d');

      // Destruir instancias anteriores para evitar superposición de gráficos
      if (this.chartEnte) {
        this.chartEnte.destroy();
      }
      if (this.chartTipo) {
        this.chartTipo.destroy();
      }

      this.chartEnte = new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: this.porEnte.map(r => r.ente),
          datasets: [{
            label: 'Empleados',
            data: this.porEnte.map(r => r.count),
            backgroundColor: 'rgba(249, 115, 22, 0.85)',
            hoverBackgroundColor: 'rgba(234, 88, 12, 0.95)',
            borderRadius: 8,
            borderSkipped: false,
            maxBarThickness: 40
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 11 } }
            },
            y: {
              grid: { color: 'rgba(148, 163, 184, 0.15)' },
              ticks: { color: '#94a3b8', font: { size: 11 } }
            }
          },
          plugins: {
            legend: { labels: { color: '#475569', font: { size: 11 } } }
          }
        }
      });
      this.chartTipo = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: this.porTipo.map(r => r.tipo),
          datasets: [{
            label: 'Participaciones',
            data: this.porTipo.map(r => r.count),
            backgroundColor: 'rgba(168, 85, 247, 0.85)',
            hoverBackgroundColor: 'rgba(124, 58, 237, 0.95)',
            borderRadius: 10,
            borderSkipped: false,
            maxBarThickness: 36
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 11 } }
            },
            y: {
              grid: { color: 'rgba(148, 163, 184, 0.15)' },
              ticks: { color: '#94a3b8', font: { size: 11 } }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
    .reportes-dashboard {
      display: grid;
      grid-template-columns: 260px minmax(0, 1fr);
      gap: 24px;
      width: 100%;
      max-width: 1400px;
      margin: 20px auto;
      padding: 0 16px 24px;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      color: #1f2933;
    }

    .sidebar {
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
      padding: 18px 16px;
      display: flex;
      flex-direction: column;
    }

    .sidebar-brand {
      font-weight: 700;
      font-size: 1rem;
      margin-bottom: 16px;
    }

    .sidebar-menu {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .sidebar-section-title {
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #9fb3c8;
      margin: 10px 0 4px;
    }

    .sidebar-item {
      all: unset;
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 0.9rem;
      color: #50627a;
      cursor: pointer;
    }

    .sidebar-item:hover {
      background: #f1f5f9;
    }

    .sidebar-item.active {
      background: #2563eb;
      color: #ffffff;
    }

    .dashboard-main {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .topbar-left h1 {
      margin: 0;
      font-size: 1.4rem;
    }

    .topbar-subtitle {
      margin-top: 4px;
      font-size: 0.85rem;
      color: #8291a7;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .pill-switch {
      background: #e5edff;
      border-radius: 999px;
      padding: 2px;
      display: inline-flex;
    }

    .pill {
      border: none;
      background: transparent;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 0.8rem;
      cursor: pointer;
      color: #4c6fff;
    }

    .pill.active {
      background: #4c6fff;
      color: #ffffff;
    }

    .date-filters {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
    }

    .date-input {
      border-radius: 6px;
      border: 1px solid #d0dbe7;
      padding: 4px 6px;
      font-size: 0.8rem;
    }

    .date-separator {
      color: #9fb3c8;
    }

    .btn-download {
      border: none;
      background: #2563eb;
      color: #ffffff;
      border-radius: 999px;
      padding: 6px 14px;
      font-size: 0.8rem;
      cursor: pointer;
      font-weight: 500;
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.35);
    }

    .btn-download:hover {
      background: #1d4ed8;
    }

    .kpi-row {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }

    .kpi-card {
      background: #ffffff;
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }

    .kpi-label {
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #9fb3c8;
    }

    .kpi-value {
      margin-top: 6px;
      font-size: 1.4rem;
      font-weight: 700;
    }

    .main-grid {
      display: grid;
      grid-template-columns: minmax(0, 2.2fr) minmax(0, 1fr);
      gap: 16px;
    }

    .card {
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
      display: flex;
      flex-direction: column;
    }

    .card-header {
      padding: 12px 16px;
      border-bottom: 1px solid #edf2f7;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .card-title {
      font-size: 0.95rem;
      font-weight: 600;
    }

    .card-subtitle {
      font-size: 0.8rem;
      color: #9fb3c8;
      margin-top: 2px;
    }

    .card-tabs {
      display: inline-flex;
      gap: 4px;
    }

    .tab {
      border-radius: 999px;
      border: none;
      padding: 4px 10px;
      font-size: 0.76rem;
      cursor: pointer;
      background: #edf2ff;
      color: #4c6fff;
    }

    .tab.active {
      background: #4c6fff;
      color: #ffffff;
    }

    .card-body {
      padding: 12px 16px 14px;
    }

    .chart-wrapper {
      height: 260px;
    }

    .bottom-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }

    .list-body ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .list-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.88rem;
    }

    .list-name {
      color: #4a5568;
    }

    .list-badge {
      background: #e5f1ff;
      color: #1d4ed8;
      border-radius: 999px;
      padding: 2px 10px;
      font-size: 0.75rem;
      font-weight: 600;
    }

    .list-badge.badge-secondary {
      background: #ecfdf5;
      color: #047857;
    }

    .empty-text {
      font-size: 0.82rem;
      color: #9fb3c8;
    }

    @media (max-width: 960px) {
      .reportes-dashboard {
        grid-template-columns: 1fr;
      }

      .sidebar {
        display: none;
      }

      .kpi-row {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .main-grid {
        grid-template-columns: 1fr;
      }

      .bottom-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 600px) {
      .topbar {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }

      .kpi-row {
        grid-template-columns: 1fr;
      }
    }
    </style>

<style>
@media print {
  @page {
    size: A4;
    margin: 10mm;
  }

  /* Ocultar todo por defecto */
  body {
    margin: 0;
  }

  body * {
    visibility: hidden;
  }

  /* Mostrar solo el dashboard de reportes */
  .reportes-dashboard,
  .reportes-dashboard * {
    visibility: visible;
  }

  .reportes-dashboard {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    /* Reducir ligeramente el tamaño para intentar que quepa en una sola hoja */
    zoom: 0.9;
  }

  /* No mostrar barra derecha (filtros + botón) ni el botón en sí */
  .reportes-dashboard .topbar-right,
  .btn-download {
    display: none !important;
  }

  /* Ajustar altura de las gráficas para evitar saltos de página */
  .chart-wrapper {
    height: 200px !important;
  }
}
</style>
