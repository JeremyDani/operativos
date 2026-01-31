<template>
  <div id="app-container">
    <header>
      <nav>
        <img src="/venezuela-flag.svg" alt="Venezuela" class="brand-flag" />
        <router-link to="/login" v-if="!authState.isAuthenticated">Login</router-link>
        <span v-if="authState.isAuthenticated">
          <router-link to="/operativos">Operativos</router-link>
          | <a href="#" @click.prevent="logout">Logout</a>
        </span>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { authState } from './auth';
import { useRouter } from 'vue-router';

const router = useRouter();

function logout() {
  authState.isAuthenticated = false;
  router.push('/login');
}
</script>

<style scoped>
#app-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

main {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 50px;
  min-height: 100vh;
  background-color: #f0f2f5;
}

header {
  background-color: #fff;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.brand-flag { height: 28px; margin-right: 12px; vertical-align: middle; }
</style>

