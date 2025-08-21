<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          🛰️ Change Detection System
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/aoi">AOI Management</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/detection">Change Detection</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/alerts">Alerts</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container-fluid mt-3">
      <router-view />
    </main>

    <footer class="bg-light text-center py-3 mt-5">
      <div class="container">
        <p class="text-muted mb-0">
          Change Detection & Monitoring System v1.0.0
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

.navbar-brand {
  font-weight: bold;
}

.nav-link {
  font-weight: 500;
}

.nav-link.router-link-active {
  color: #fff !important;
  font-weight: 600;
}
</style>

