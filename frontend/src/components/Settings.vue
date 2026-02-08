<template>
  <div class="settings-container">
    <h2>Ajustes</h2>
    <p>Esta es la página de ajustes. Añade aquí las opciones de configuración del usuario.</p>
    <div class="setting-item">
      <label>Notificaciones</label>
      <input type="checkbox" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings'
}
</script>

<style scoped>
.settings-container{max-width:900px;margin:80px auto;padding:24px;background:#fff;border-radius:8px;box-shadow:0 8px 24px rgba(15,23,42,0.06)}
.settings-container h2{margin-top:0}
.setting-item{margin-top:16px;display:flex;align-items:center;gap:12px}
</style>
