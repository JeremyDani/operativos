import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: { nombre: '', email: '', roles: [] }
  }),
  getters: {
    hasRole: (state) => (role) => state.user.roles.includes(role),
    hasAnyRole: (state) => (roles) => roles.some(r => state.user.roles.includes(r))
  },
  actions: {
    setUser(payload) {
      this.isAuthenticated = true
      this.user = payload
    },
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
