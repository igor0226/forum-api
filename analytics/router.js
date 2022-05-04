import VueRouter from 'vue-router';
import Reports from './src/pages/Reports/Reports.vue';
import Wiki from './src/pages/Wiki/Wiki.vue';

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/reports',
            name: 'reports',
            component: Reports,
        },
        {
            path: '/',
            name: 'wiki',
            component: Wiki,
        },
    ],
});
