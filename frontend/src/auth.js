// Estado reactivo compartido para controlar la autenticación en el frontend.
// Otros componentes importan `authState` para mostrar/ocultar elementos.
import { reactive } from 'vue';

export const authState = reactive({
  // `true` cuando el usuario está logueado; usado en `App.vue` y componentes.
  isAuthenticated: false,
  // información básica para mostrar en el header (puede actualizarse tras login)
  user: {
    nombre: '',
    email: '',
    roles: []
  }
});
