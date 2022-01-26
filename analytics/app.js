import Vue from 'vue';
import VueMaterial from 'vue-material';
import VueRouter from 'vue-router';
import router from './router';
import App from './App.vue';
import './src/components/registry';

import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

Vue.config.productionTip = false;

Vue.use(VueMaterial);
Vue.use(VueRouter);

// eslint-disable-next-line
new Vue({
    el: '#app',
    router,
    components: { App },
    render: h => h(App),
});
