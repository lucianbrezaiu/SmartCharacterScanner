import Vue from 'vue';
import App from './App.vue';
import router from './router';

import { BProgress } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';

Vue.use(BootstrapVue);
Vue.config.productionTip = false;

Vue.component('b-progress', BProgress)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
