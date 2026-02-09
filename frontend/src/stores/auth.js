import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: {
      // Nombre mostrado en cabecera / perfil (puede venir de nombre_apellido o username)
      nombre: '',
      // Id interno del usuario en la base de datos
      id: null,
      // Nombre y apellido completos tal como están en el backend
      nombre_apellido: '',
      // Identificador de usuario
      username: '',
      // Correo electrónico
      email: '',
      // Prefijo de origen (V/E) y número de cédula
      origen: '',
      cedula: null,
      // Roles/grupos asignados en Django
      roles: []
    },
    // Tema visual de la aplicación: 'light' o 'dark'
    theme: 'light'
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
      // Mezclar sobre la estructura base para no perder propiedades
      this.user = { ...this.user, ...payload }
    },
    // Limpia completamente la información de autenticación y usuario
    clear() {
      this.isAuthenticated = false
      this.user = {
        nombre: '',
        id: null,
        nombre_apellido: '',
        username: '',
        email: '',
        origen: '',
        cedula: null,
        roles: []
      }
      this.theme = 'light'
    },
    setTheme(theme) {
      this.theme = theme === 'dark' ? 'dark' : 'light'
    }
  },
  // Persistir el store en localStorage usando pinia-plugin-persistedstate
  // No persistimos `isAuthenticated` para evitar logins automáticos tras recarga.
  // Persistimos sólo `user` para facilitar ciertas pestañas, pero la sesión
  // deberá autenticarse cada vez en desarrollo.
  persist: {
    // Usar sessionStorage para que, al cerrar la pestaña/ventana,
    // se borre la información de usuario y se requiera login de nuevo.
    storage: sessionStorage,
    paths: ['user', 'theme']
  }
})
