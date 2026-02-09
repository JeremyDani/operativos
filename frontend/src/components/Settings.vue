<template>
  <div class="settings-container">
    <h2>Ajustes</h2>
    <p>Esta es la página de ajustes. Aquí se podrán agregar opciones de configuración del usuario.</p>

    <div class="setting-item">
      <button type="button" class="setting-button" @click="openPasswordModal">
        <span class="setting-label">Cambio de contraseña</span>
        <span class="setting-hint">Haz clic para cambiar tu contraseña</span>
      </button>
    </div>

    <!-- Modal de cambio de contraseña -->
    <div v-if="showPasswordModal" class="modal-overlay" @click.self="closePasswordModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Cambio de contraseña</h3>
          <button type="button" class="modal-close" @click="closePasswordModal">×</button>
        </div>

        <form class="password-form" @submit.prevent="handleChangePassword">
          <div class="form-row">
            <label for="old-password">Contraseña actual</label>
            <input
              id="old-password"
              type="password"
              v-model="oldPassword"
              required
            />
          </div>
          <div class="form-row">
            <label for="new-password">Nueva contraseña</label>
            <input
              id="new-password"
              type="password"
              v-model="newPassword"
              required
            />
          </div>
          <div class="form-row">
            <label for="confirm-password">Confirmar nueva contraseña</label>
            <input
              id="confirm-password"
              type="password"
              v-model="confirmPassword"
              required
            />
          </div>

          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="closePasswordModal">Cancelar</button>
            <button type="submit" class="btn-primary">Guardar nueva contraseña</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Settings',
  setup() {
    const auth = useAuthStore();
    const showPasswordModal = ref(false);
    const oldPassword = ref('');
    const newPassword = ref('');
    const confirmPassword = ref('');
    const errorMessage = ref('');
    const successMessage = ref('');

    const openPasswordModal = () => {
      errorMessage.value = '';
      successMessage.value = '';
      showPasswordModal.value = true;
    };

    const closePasswordModal = () => {
      showPasswordModal.value = false;
    };

    const handleChangePassword = async () => {
      errorMessage.value = '';
      successMessage.value = '';

      if (!auth.user || auth.user.id == null) {
        errorMessage.value = 'No se pudo identificar el usuario actual.';
        return;
      }

      if (newPassword.value !== confirmPassword.value) {
        errorMessage.value = 'La nueva contraseña y la confirmación no coinciden.';
        return;
      }

      try {
        const payload = {
          user_id: auth.user.id,
          old_password: oldPassword.value,
          new_password: newPassword.value
        };
        const res = await axios.post('/api/auth/change-password', payload);

        if (res.status === 200) {
          successMessage.value = res.data.message || 'Contraseña actualizada correctamente.';
          oldPassword.value = '';
          newPassword.value = '';
          confirmPassword.value = '';
        } else {
          errorMessage.value = res.data.message || 'No se pudo cambiar la contraseña.';
        }
      } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
          errorMessage.value = error.response.data.message;
        } else {
          errorMessage.value = 'Error al intentar cambiar la contraseña.';
        }
        console.error('Error cambiando contraseña:', error);
      }
    };

    return {
      showPasswordModal,
      openPasswordModal,
      closePasswordModal,
      oldPassword,
      newPassword,
      confirmPassword,
      errorMessage,
      successMessage,
      handleChangePassword
    };
  }
}
</script>

<style scoped>
.settings-container{max-width:900px;margin:80px auto;padding:24px;background:#fff;border-radius:8px;box-shadow:0 8px 24px rgba(15,23,42,0.06)}
.settings-container h2{margin-top:0}
.setting-item{margin-top:16px;display:flex;align-items:center;gap:12px}
.setting-button{width:100%;display:flex;flex-direction:column;align-items:center;padding:10px 12px;border-radius:6px;border:1px solid #e5e7eb;background:#f9fafb;cursor:pointer;transition:background-color .15s ease,border-color .15s ease,box-shadow .15s ease}
.setting-button:hover{background:#eff6ff;border-color:#bfdbfe;box-shadow:0 2px 6px rgba(59,130,246,.15)}
.setting-label{font-weight:600;text-align:center;width:100%}
.setting-hint{font-size:.85rem;color:#6b7280;margin-top:2px;text-align:center;width:100%}
.password-form{margin-top:12px;display:flex;flex-direction:column;gap:12px;max-width:420px}
.form-row{display:flex;flex-direction:column;gap:4px}
.form-row input{padding:6px 8px;border:1px solid #d1d5db;border-radius:4px}
.btn-primary{align-self:flex-start;padding:8px 14px;border:none;border-radius:6px;background:#0d6efd;color:#fff;cursor:pointer;font-weight:600}
.btn-primary:active{transform:translateY(1px)}
.error-message{color:#b91c1c;font-size:0.85rem}
.success-message{color:#15803d;font-size:0.85rem}
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,.5);display:flex;align-items:center;justify-content:center;z-index:2000}
.modal-content{background:#fff;border-radius:8px;max-width:480px;width:90%;padding:20px 24px;box-shadow:0 16px 40px rgba(15,23,42,.35)}
.modal-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.modal-header h3{margin:0;font-size:1.1rem}
.modal-close{border:none;background:transparent;font-size:1.2rem;cursor:pointer;line-height:1}
.modal-actions{margin-top:8px;display:flex;gap:8px;justify-content:flex-end}
.btn-secondary{padding:8px 14px;border-radius:6px;border:1px solid #d1d5db;background:#f9fafb;cursor:pointer;font-weight:500}
.btn-secondary:active{transform:translateY(1px)}
</style>
