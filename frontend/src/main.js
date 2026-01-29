import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Bootstrap (CSS + JS) and icons
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// your app CSS (kept minimal; will override any old global rules)
import './assets/main.css'

createApp(App).use(router).mount('#app')
