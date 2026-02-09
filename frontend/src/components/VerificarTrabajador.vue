<template>
  <!-- Pantalla para verificar la cédula de un trabajador y registrar su participación -->
  <div class="verificar-container">
    <div class="verificar-card">
    <h1>Demostrador</h1>
    <div class="verificar-form">
      <div class="input-row">
        <label for="origin-select" class="origin-label">
          <span>Origen</span>
          <!-- Selección de prefijo V/E que se antepone a la cédula si el usuario no lo ingresa -->
          <select id="origin-select" v-model="originSelection" class="origin-select">
            <option value="V">V</option>
            <option value="E">E</option>
          </select>
        </label>
        <!-- Input de cédula; Enter y botón llaman a `verificarCedula()` -->
        <input class="cedula-input" type="text" v-model="cedula" placeholder="Número de Cédula" @keyup.enter="verificarCedula"/>
      </div>

      <!-- Botón grande estilo barra verde de la captura -->
      <div class="verify-bar">
        <button class="big-verify" @click="verificarCedula">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right:8px;">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1 1 0 0 0 1.415-1.415l-3.85-3.85zm-5.242 0a5 5 0 1 1 0-10 5 5 0 0 1 0 10z"/>
          </svg>
          Verificar
        </button>
      </div>
    </div>
    <div v-if="loading">Cargando...</div>
    <div v-if="mensaje" class="mensaje" :class="mensajeTipo">{{ mensaje }}</div>

    <!-- Modal: muestra datos del operativo y datos de la nómina para confirmar participación -->
    <div v-if="modalVisible" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
    <h2>Datos del Trabajador</h2>
  </div>

        <div class="modal-body info-grid">
          <div class="row"><span class="key">Ente:</span><span class="val">{{ trabajador.ente || '-' }}</span></div>
          <div class="row"><span class="key">Origen y Cédula:</span><span class="val">{{ trabajador.cedula || (originSelection + cedula) }}</span></div>
          <div class="row"><span class="key">Nombre y Apellido:</span><span class="val">{{ (trabajador.nombres || '-') + (trabajador.apellidos ? (' ' + trabajador.apellidos) : '') }}</span></div>
        </div>

        <div class="modal-actions split">
          <button class="btn-confirm" :disabled="!cedulaMatchesOrigin" @click="confirmarParticipacion">Confirmar</button>
          <button class="btn-cancel" @click="closeModal">Cancelar</button>
        </div>
      </div>
    </div>
    <!-- Modal de error simple -->
    <div v-if="errorModalVisible" class="modal-overlay" @click="errorModalVisible = false">
      <div class="modal-content" @click.stop>
        <h2>Trabajador no encontrado</h2>
        <div class="modal-actions">
          <button class="btn-cancel" @click="errorModalVisible = false">Aceptar</button>
        </div>
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

              axios.get(`/api/operativos/${operativoId}/verificar/${requestCedula}`)
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
                    // Mostrar mensaje simplificado indicando participación reciente
                    this.mensaje = 'Este usuario participo recientemente en el operativo';
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
                    return axios.get(`/api/libro/${operativoId}`)
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
              axios.post(`/api/operativos/${operativoId}/guardar-participacion`, payload)
                .then(response => {
                  // Mostrar mensaje corto y consistente en frontend,
                  // ignorando detalles extensos que pueda devolver el backend.
                  this.mensaje = 'Participacion registrada';
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
          /* Fondo a pantalla casi completa para la vista de verificación */
          min-height: calc(100vh - 60px);
          width: 100%;
          padding: 40px 20px;
          display: flex;
          justify-content: center;
          align-items: flex-start;
          /* Usa la misma imagen de fondo que /operativos */
          background-image: url('/fondo%20frontend.jpg');
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
        }

        .verificar-card {
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
          display: block;
          gap: 10px;
        }
        .input-row{display:flex;align-items:center;gap:8px}
        .origin-label{display:flex;align-items:center;gap:6px;font-weight:600}
        .origin-select{padding:8px;border-radius:6px;border:1px solid #dcdcdc;background:#fff}
        .cedula-input{flex:1;padding:12px;border-radius:6px;border:1px solid #dcdcdc}

        .verify-bar{margin-top:12px}
        .big-verify{width:100%;display:inline-flex;align-items:center;justify-content:center;padding:12px 16px;background:#0d6efd;color:#fff;border:none;border-radius:6px;font-weight:600;cursor:pointer;box-shadow:0 6px 18px rgba(13,110,253,0.25)}
        .big-verify:hover{background:#0b5ed7}
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
        .modal-header{padding:12px 16px;border-bottom:1px solid #eee}
        .modal-header h2{margin:0;font-size:1.1rem}
        .modal-body.info-grid{padding:16px 18px;background:#fafafa}
        .info-grid .row{display:flex;padding:8px 0;border-bottom:1px solid #f0f0f0}
        .info-grid .key{flex:0 0 220px;color:#666;font-weight:600}
        .info-grid .val{flex:1;color:#222}

        .modal-actions { display:flex; gap:12px; padding:16px; }
        .modal-actions.split{justify-content:space-between}
        .btn-confirm { background:#0d6efd; color:#fff; padding:10px 18px; border:none; border-radius:6px; cursor:pointer; flex:1 }
        .btn-confirm:disabled{opacity:0.6;cursor:not-allowed}
         .btn-cancel { background:#0b5ed7; color:#fff; padding:10px 18px; border:none; border-radius:6px; cursor:pointer; flex:1 }
        /* Logout button removed */
        </style>
