import Vue from 'vue';
import App from './App';
import VueMaterial from 'vue-material';
import VueRouter from 'vue-router';
import { router } from './router';

import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css';

Vue.config.productionTip = false;

Vue.use(VueMaterial);
Vue.use(VueRouter);

new Vue({
    el: '#app',
    router,
    components: { App },
    render: h => h(App),
});
