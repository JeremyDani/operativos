<template>
  <div class="verificar-container">
    <h1>Verificar Trabajador</h1>
    <div class="verificar-form">
      <div style="display:flex;align-items:center;gap:8px;">
        <label for="origin-select" style="display:flex;align-items:center;gap:6px;">
          <span style="font-weight:600;">Origen</span>
          <select id="origin-select" v-model="originSelection" style="padding:6px;border-radius:4px;border:1px solid #ccc;">
            <option value="V">V - Venezolano</option>
            <option value="E">E - Extranjero</option>
          </select>
        </label>
        <input type="text" v-model="cedula" placeholder="Ingrese la cédula del trabajador" @keyup.enter="verificarCedula"/>
        <button @click="verificarCedula">Verificar</button>
      </div>
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
          <!-- Origen selector removed from modal (kept at top of page) -->
        </div>
        <div class="modal-actions">
          <button class="btn-continue" :disabled="!cedulaMatchesOrigin" @click="confirmarParticipacion">Continuar</button>
          <button class="btn-cancel" @click="closeModal">Cancelar</button>
        </div>
      </div>
    </div>
    <!-- Modal de error simple -->
    <div v-if="errorModalVisible" class="modal-overlay" @click="errorModalVisible = false">
      <div class="modal-content" @click.stop>
        <h2>Trabajador no encontrado</h2>
        <p>La cédula no coincide con el origen seleccionado.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="errorModalVisible = false">Aceptar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
        import axios from 'axios';
        import { authState } from '../auth';

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
              errorModalVisible: false,
              operativo: {},
              trabajador: {},
              authState,
                  alreadyParticipated: false,
                  lastParticipation: null,
                  originSelection: 'V'
            };
          },
              computed: {
                cedulaMatchesOrigin() {
                  const ced = String(this.trabajador.cedula || this.cedula || '');
                  if (!ced) return false;
                  const first = ced.charAt(0).toUpperCase();
                  return first === (this.originSelection || '').toUpperCase();
                }
              },
          methods: {
            logout() {
              try {
                this.authState.isAuthenticated = false;
              } catch (e) {}
              this.$router.push('/login');
            },
            verificarCedula() {
              if (!this.cedula) {
                this.mensaje = 'Por favor, ingrese una cédula.';
                this.mensajeTipo = 'error';
                this.resultado = null;
                return;
              }
              // Allow numeric cédula input without prefix. If the user
              // includes a prefix (V/E) ensure it matches the selected origin.
              const cedCheck = String(this.cedula || '').trim();
              const hasPrefix = /^[VE]/i.test(cedCheck);
              if (hasPrefix && cedCheck.charAt(0).toUpperCase() !== (this.originSelection || '').toUpperCase()) {
                this.mensaje = 'Trabajador no encontrado.';
                this.mensajeTipo = 'error';
                this.resultado = null;
                this.errorModalVisible = true;
                return;
              }
              this.loading = true;
              this.mensaje = '';
              this.resultado = null;
              const operativoId = this.$route.params.id;

              // Build the request cedula: if user entered numeric without prefix,
              // prepend the selected origin so backend receives e.g. 'V30551654'.
              const requestCedula = hasPrefix ? cedCheck : `${(this.originSelection||'V')}${cedCheck}`;

              axios.get(`http://localhost:8000/api/operativos/${operativoId}/verificar/${requestCedula}`)
                .then(response => {
                  const data = response.data;
                  // Si existe registro histórico, informar y no abrir modal
                  if (data.participacion_historica) {
                    this.alreadyParticipated = true;
                    this.lastParticipation = data.participacion_historica.history_date || null;
                    this.trabajador = data.trabajador || {
                      cedula: this.cedula,
                      nombres: data.participacion_historica.nombres,
                      apellidos: data.participacion_historica.apellidos,
                      cargo: data.participacion_historica.cargo,
                      ente: data.participacion_historica.ente,
                      origen: data.participacion_historica.origen || null
                    };
                    const origenText = data.participacion_historica.origen ? ` (origen: ${data.participacion_historica.origen})` : '';
                    this.mensaje = `Esta cédula ya registró participación el ${this.lastParticipation || 'fecha desconocida'}${origenText}.`;
                    this.mensajeTipo = 'info';
                    this.modalVisible = false;
                    return;
                  }

                  if (data.encontrado) {
                    const trabajadorData = data.trabajador || {};
                    // Si el trabajador encontrado tiene cédula con prefijo, validar
                    // que coincida con la selección del usuario. Si no coincide,
                    // mostrar error y NO abrir el modal con datos del operativo.
                    const ced = String(trabajadorData.cedula || '');
                    const foundPrefix = /^[VE]/i.test(ced) ? ced.charAt(0).toUpperCase() : null;
                    if (foundPrefix && foundPrefix !== (this.originSelection || '').toUpperCase()) {
                      this.mensaje = 'Trabajador no encontrado.';
                      this.mensajeTipo = 'error';
                      this.resultado = null;
                      this.errorModalVisible = true;
                      return;
                    }

                    this.trabajador = trabajadorData;
                    // fetch operativo details
                    return axios.get(`http://localhost:8000/api/libro/${operativoId}`)
                      .then(r => {
                            this.operativo = r.data;
                            // NO sobrescribir `originSelection` aquí: conservar la elección del usuario
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
              // Usar origen seleccionado en el modal
              const origen = (this.originSelection || '').toUpperCase();
              payload.origen = origen;
              // Validar coincidencia entre cédula y origen antes de enviar
              const ced = String(payload.cedula || '');
              if (!/^[VE]/i.test(ced) || ced.charAt(0).toUpperCase() !== origen) {
                this.mensaje = `La cédula ${ced} no coincide con el origen seleccionado (${origen}).`;
                this.mensajeTipo = 'error';
                return;
              }
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
        /* Logout button removed */
        </style>
