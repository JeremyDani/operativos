<template>
  <!-- Lista principal de operativos: muestra tablas y modal de detalles -->
  <div class="operativos-container">
    <h1>Lista de Operativos</h1>

    <div class="operativos-card">
      <div class="card-header">
        <span>Seleccione un Operativo</span>
      </div>
      <div class="card-body">

    <!-- Mensaje de notificación breve (success/error) -->
    <div v-if="notification.message" :class="['notification', notification.type]">
      {{ notification.message }}
    </div>

    <div v-if="loading">Cargando...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <!-- Indicador de filtro por fecha -->
    <div v-if="selectedDate" class="date-filter-banner">
      Mostrando operativos para: {{ selectedDate }}
      <button type="button" class="clear-filter" @click="clearDateFilter">Quitar filtro</button>
    </div>

    <!-- Lista de operativos (fila por fila) -->
    <div v-if="filteredOperativos.length" class="operativos-list">
      <div class="list-row" v-for="operativo in filteredOperativos" :key="operativo.id" @click="$router.push({ name: 'VerificarTrabajador', params: { id: operativo.id } })">
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
    <p v-if="!loading && !filteredOperativos.length">No se encontraron operativos.</p>

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

    <!-- Modal emergente para calendario de operativos -->
    <div v-if="showCalendar" class="calendar-modal-overlay" @click="toggleCalendar">
      <div class="calendar-modal" @click.stop>
        <div class="calendar-modal-header">
          <h2>Calendario de operativos</h2>
          <button type="button" class="calendar-close" @click="toggleCalendar">&times;</button>
        </div>
        <div class="calendar-popup">
          <div class="calendar-header">
            <button class="month-nav" @click="prevMonth">&#8249;</button>
            <span class="calendar-title">{{ calendarMonthLabel }}</span>
            <button class="month-nav" @click="nextMonth">&#8250;</button>
          </div>
          <table class="calendar-table">
            <thead>
              <tr>
                <th>D</th>
                <th>L</th>
                <th>M</th>
                <th>M</th>
                <th>J</th>
                <th>V</th>
                <th>S</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(week, wIndex) in calendarWeeks" :key="wIndex">
                <td v-for="(cell, cIndex) in week" :key="cIndex" class="calendar-cell">
                  <div
                    v-if="cell"
                    class="calendar-day"
                    :class="{ 'selected-day': selectedDate === cell.ymd }"
                    @click="onCalendarDayClick(cell.ymd)"
                  >
                    <span class="day-number">{{ cell.day }}</span>
                    <span
                      v-if="operativosByDate[cell.ymd] && operativosByDate[cell.ymd].red"
                      class="dot dot-red"
                      title="Operativos iniciados"
                    ></span>
                    <span
                      v-if="operativosByDate[cell.ymd] && operativosByDate[cell.ymd].green"
                      class="dot dot-green"
                      title="Operativos por iniciar"
                    ></span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="calendar-legend">
            <span class="legend-item">
              <span class="dot dot-red"></span> Ya iniciaron
            </span>
            <span class="legend-item">
              <span class="dot dot-green"></span> Por iniciar
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Componente que obtiene la lista de operativos desde `/api/libro/` y muestra detalles
import axios from 'axios';

const MONTHS = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

export default {
  data() {
    const today = new Date();
    return {
      operativos: [],
      loading: true,
      error: null,
      selectedOperativo: null,
      notification: {
        message: '',
        type: '' // 'success' o 'error'
      },
      // Controla la visibilidad del calendario de resumen
      showCalendar: false,
      // Mes y año actualmente visibles en el calendario
      calendarYear: today.getFullYear(),
      calendarMonth: today.getMonth(), // 0 = enero
      // Fecha seleccionada desde el calendario (YYYY-MM-DD) para filtrar la lista
      selectedDate: null
    };
  },
  computed: {
    // Mapea fechas (YYYY-MM-DD) a cantidad de operativos ya iniciados (rojo)
    // o por iniciar (verde) según la fecha de inicio.
    operativosByDate() {
      const map = {};
      const todayYMD = new Date().toISOString().slice(0, 10);

      this.operativos.forEach(o => {
        if (!o.fecha_inicio) return;
        const d = new Date(o.fecha_inicio);
        if (Number.isNaN(d.getTime())) return;
        const ymd = d.toISOString().slice(0, 10);
        const status = ymd <= todayYMD ? 'started' : 'upcoming';
        if (!map[ymd]) {
          map[ymd] = { red: 0, green: 0 };
        }
        if (status === 'started') {
          map[ymd].red += 1;
        } else {
          map[ymd].green += 1;
        }
      });

      return map;
    },
    // Lista de operativos filtrada por la fecha seleccionada en el calendario
    filteredOperativos() {
      if (!this.selectedDate) {
        return this.operativos;
      }
      return this.operativos.filter(o => {
        if (!o.fecha_inicio) return false;
        const d = new Date(o.fecha_inicio);
        if (Number.isNaN(d.getTime())) return false;
        const ymd = d.toISOString().slice(0, 10);
        return ymd === this.selectedDate;
      });
    },
    // Matriz de semanas para el mes actual (para mostrar en el calendario)
    calendarWeeks() {
      const year = this.calendarYear;
      const month = this.calendarMonth;
      const first = new Date(year, month, 1);
      const firstWeekday = first.getDay(); // 0 = domingo
      const daysInMonth = new Date(year, month + 1, 0).getDate();

      const cells = [];
      for (let i = 0; i < firstWeekday; i += 1) {
        cells.push(null);
      }
      for (let day = 1; day <= daysInMonth; day += 1) {
        const date = new Date(year, month, day);
        const ymd = date.toISOString().slice(0, 10);
        cells.push({ day, ymd });
      }

      const weeks = [];
      for (let i = 0; i < cells.length; i += 7) {
        weeks.push(cells.slice(i, i + 7));
      }
      return weeks;
    },
    calendarMonthLabel() {
      return `${MONTHS[this.calendarMonth]} ${this.calendarYear}`;
    }
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
    },
    onCalendarDayClick(ymd) {
      // Si se vuelve a hacer clic sobre la misma fecha, se limpia el filtro
      if (this.selectedDate === ymd) {
        this.selectedDate = null;
      } else {
        this.selectedDate = ymd;
      }
      // Cerrar el calendario emergente al seleccionar
      this.toggleCalendar();
    },
    toggleCalendar() {
      this.showCalendar = !this.showCalendar;
      // Al abrir por primera vez, asegurarse de estar en el mes/año actual
      if (this.showCalendar) {
        const today = new Date();
        this.calendarYear = today.getFullYear();
        this.calendarMonth = today.getMonth();
      }
    },
    nextMonth() {
      if (this.calendarMonth === 11) {
        this.calendarMonth = 0;
        this.calendarYear += 1;
      } else {
        this.calendarMonth += 1;
      }
    },
    prevMonth() {
      if (this.calendarMonth === 0) {
        this.calendarMonth = 11;
        this.calendarYear -= 1;
      } else {
        this.calendarMonth -= 1;
      }
    },
    clearDateFilter() {
      this.selectedDate = null;
    }
  },
  mounted() {
    this.fetchOperativos(); // Cargar datos al montar
    // Escuchar el evento global disparado desde el icono de calendario del header
    window.addEventListener('toggle-operativos-calendar', this.toggleCalendar);
  },
  beforeUnmount() {
    window.removeEventListener('toggle-operativos-calendar', this.toggleCalendar);
  }
};
</script>

<style scoped>
.operativos-container {
  /* Fondo a pantalla completa para la vista de operativos */
  min-height: calc(100vh - 60px); /* 100vh menos el alto aproximado del header fijo */
  width: 100%;
  padding: 40px 20px;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* Usa la imagen ubicada en frontend/public/fondo frontend.jpg */
  background-image: url('/fondo%20frontend.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #1f2933;
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
.operativos-card{background: rgba(255,255,255,0.96);border-radius:10px;box-shadow:0 12px 30px rgba(15,23,42,0.16);overflow:hidden;max-width:900px;width:100%}
.card-header{padding:14px 18px;font-weight:700;background:transparent;color:#333;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center}
.card-body{padding:0}

.calendar-popup {
  padding: 10px 18px 16px;
  background: #fafafa;
}

.calendar-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 4px;
  gap: 10px;
}

.calendar-title {
  font-size: 0.9rem;
  font-weight: 600;
}

.month-nav {
  border: none;
  background-color: #e5e7eb;
  border-radius: 999px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  color: #374151;
  transition: background-color 0.15s ease, transform 0.1s ease;
}

.month-nav:hover {
  background-color: #d1d5db;
}

.month-nav:active {
  transform: scale(0.96);
}

.calendar-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
}

.calendar-table th,
.calendar-table td {
  text-align: center;
  padding: 2px 0;
}

.calendar-cell {
  height: 22px;
}

.calendar-day {
  position: relative;
  cursor: pointer;
}

.day-number {
  display: block;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  display: inline-block;
  margin: 0 1px;
}

.dot-red {
  background: #ef4444;
}

.dot-green {
  background: #22c55e;
}

.selected-day {
  background-color: #e0f2fe;
  border-radius: 6px;
}

.calendar-legend {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 4px;
  font-size: 0.75rem;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.calendar-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1500;
}

.calendar-modal {
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.35);
  max-width: 480px;
  width: 100%;
  padding: 10px 0 14px;
}

.calendar-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 18px 4px;
  border-bottom: 1px solid #e5e7eb;
}

.calendar-modal-header h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.calendar-close {
  border: none;
  background: transparent;
  font-size: 1.2rem;
  cursor: pointer;
}

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

.date-filter-banner {
  margin-top: 12px;
  margin-bottom: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  background-color: rgba(59, 130, 246, 0.08);
  color: #1d4ed8;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.clear-filter {
  border: none;
  background: transparent;
  color: #1d4ed8;
  cursor: pointer;
  font-size: 0.8rem;
  text-decoration: underline;
}

/* Responsive: make list rows stack and allow content to wrap */
@media (max-width: 720px) {
  .operativos-container { padding: 20px 12px; min-height: 100vh; }
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
