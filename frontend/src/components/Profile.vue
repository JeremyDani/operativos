<template>
  <div class="profile-container">
    <h2>Perfil</h2>
    <p>Nombre: Usuario</p>
    <p>Email: usuario@ejemplo.local</p>
    <p>Rol: Demo</p>
  </div>
</template>

<script>
export default {
  name: 'Profile'
}
</script>

<style scoped>
.profile-container{max-width:720px;margin:80px auto;padding:20px;background:#fff;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.06)}
.profile-container h2{margin-top:0}
</style>
