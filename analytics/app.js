import Vue from 'vue';
import VueMaterial from 'vue-material';
import VueRouter from 'vue-router';
import { router } from './router';
import App from './App';
import Header from './src/components/Header/Header';

import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

Vue.config.productionTip = false;

Vue.use(VueMaterial);
Vue.use(VueRouter);

// TODO: make components registry
Vue.component('page-header', Header);

// eslint-disable-next-line
new Vue({
    el: '#app',
    router,
    components: { App },
    render: h => h(App),
});
