import Router from 'vue-router';
import Reports from './src/pages/Reports/Reports';

export const router = new Router({
    routes: [
        {
            path: '/',
            name: 'reports',
            component: Reports,
        }
    ],
});
