import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueRouter from 'vue-router'
import router from './router'
import axios from 'axios'
import qs from 'qs'

Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios
Vue.prototype.qs = qs   //全局注册，使用方法为:this.qs
Vue.use(VueRouter);
Vue.use(ElementUI, { size: 'small' });

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
