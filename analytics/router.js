import Router from 'vue-router';
import Reports from './src/pages/Reports/Reports.vue';

export default new Router({
    routes: [
        {
            path: '/',
            name: 'reports',
            component: Reports,
        },
    ],
});
