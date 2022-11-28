import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Prescription from './components/Prescription.vue'
Vue.config.productionTip = false
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import VueSpeech from 'vue-speech'
 
 
Vue.use(VueSpeech)
// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.productionTip = false
Vue.prototype.$http = axios;
Vue.use(VueRouter);

const routes = [
  { path: '/', component: Prescription },
  
]

const router = new VueRouter({
  routes
})


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
