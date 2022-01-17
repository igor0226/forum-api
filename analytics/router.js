import Router from 'vue-router';
import Main from './src/pages/Main/Main';

export const router = new Router({
    routes: [
        {
            path: '/',
            name: 'main',
            component: Main,
        }
    ],
});
