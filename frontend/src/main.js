import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import HelloWorld from './components/HelloWorld'
Vue.config.productionTip = false
import axios from 'axios'


Vue.config.productionTip = false
Vue.prototype.$http = axios;
Vue.use(VueRouter);

const routes = [
  { path: '/', component: HelloWorld },
  
]

const router = new VueRouter({
  routes
})


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
