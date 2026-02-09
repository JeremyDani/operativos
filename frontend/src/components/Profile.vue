<template>
  <div class="profile-container">
    <h2>Perfil de usuario</h2>
    <p><strong>Nombre y apellido:</strong> {{ user.nombre_apellido || user.nombre }}</p>
    <p><strong>Número de cédula:</strong> {{ formattedCedula || '—' }}</p>
    <p><strong>Correo:</strong> {{ user.email || '—' }}</p>
    <p><strong>Rol(es):</strong> {{ user.roles && user.roles.length ? user.roles.join(', ') : 'Sin rol asignado' }}</p>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Profile',
  setup() {
    const auth = useAuthStore();
    const user = computed(() => auth.user || {});

    const formattedCedula = computed(() => {
      if (!user.value || user.value.cedula == null || user.value.cedula === '') {
        return '';
      }
      const prefix = user.value.origen || '';
      const numero = String(user.value.cedula);
      return prefix ? `${prefix}-${numero}` : numero;
    });

    return {
      user,
      formattedCedula
    };
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 720px;
  margin: 80px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
}

.profile-container h2 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.profile-container p {
  margin: 0.3rem 0;
}
</style>
