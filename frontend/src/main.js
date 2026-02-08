// Punto de entrada del frontend: crea la app de Vue, instala el router
// y monta la aplicación en el elemento `#app` del `index.html`.
import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Importar el router
import { createPinia } from 'pinia'
import axios from 'axios'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { useAuthStore } from './stores/auth'



const app = createApp(App)
// Pinia: store global
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
// En desarrollo: asegurar que la sesión local no fuerce rutas protegidas.
// Eliminamos cualquier clave previa de Pinia y limpiamos el store antes
// de que el router procese la ruta inicial. Esto evita que la SPA arranque
// en `/operativos` por estados persistidos antiguos.
if (typeof window !== 'undefined' && import.meta.env.DEV) {
	try {
		localStorage.removeItem('pinia');
	} catch (e) {
		// no-op
	}
	try {
		const auth = useAuthStore();
		// Garantizar estado limpio
		auth.clear();
		if (window && window.location && window.location.pathname && window.location.pathname !== '/login') {
			window.history.replaceState({}, '', '/login');
		}
	} catch (e) {
		// no-op
	}
}
// Registrar el router para que `<router-view>` y `<router-link>` funcionen
app.use(router)

// Habilitar envío de credenciales en axios para que la cookie de sesión se preserve
// cuando se usa el proxy de Vite (útil en desarrollo).
axios.defaults.withCredentials = true

// En desarrollo: asegurar que la sesión local no fuerce rutas protegidas.
// Ejecutar limpieza una vez que Pinia y el router estén registrados.
if (typeof window !== 'undefined' && import.meta.env.DEV) {
	try {
		localStorage.removeItem('pinia');
	} catch (e) {
		// no-op
	}
	try {
		const auth = useAuthStore();
		// Garantizar estado limpio
		auth.clear();
		if (window && window.location && window.location.pathname && window.location.pathname !== '/login') {
			window.history.replaceState({}, '', '/login');
		}
	} catch (e) {
		// no-op
	}
}

// Montar la aplicación en el DOM
app.mount('#app')

