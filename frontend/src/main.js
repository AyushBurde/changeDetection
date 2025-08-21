import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Create Vue application
const app = createApp(App)

// Use plugins
app.use(router)
app.use(store)

// Mount the application
app.mount('#app')

