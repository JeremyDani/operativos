import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: { nombre: '', email: '', roles: [] }
  }),
  getters: {
    // Devuelve true si el usuario tiene exactamente ese rol
    hasRole: (state) => (role) => state.user.roles.includes(role),
    // Devuelve true si el usuario tiene al menos uno de los roles indicados
    hasAnyRole: (state) => (roles) => roles.some(r => state.user.roles.includes(r))
  },
  actions: {
    // Marca la sesión como autenticada y guarda el payload del usuario (incluye roles)
    setUser(payload) {
      this.isAuthenticated = true
      this.user = payload
    },
    // Limpia completamente la información de autenticación y usuario
    clear() {
      this.isAuthenticated = false
      this.user = { nombre: '', email: '', roles: [] }
    }
  },
  // Persistir el store en localStorage usando pinia-plugin-persistedstate
  // No persistimos `isAuthenticated` para evitar logins automáticos tras recarga.
  // Persistimos sólo `user` para facilitar ciertas pestañas, pero la sesión
  // deberá autenticarse cada vez en desarrollo.
  persist: {
    paths: ['user']
  }
})
