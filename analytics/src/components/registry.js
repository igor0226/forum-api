import Vue from 'vue';
import VueApexCharts from 'vue-apexcharts'
import Header from './Header/Header.vue';
import Fragment from './Fragment/Fragment.vue';
import ApiCard from './ApiCard/ApiCard.vue';

Vue.component('page-header', Header);
Vue.component('app-fragment', Fragment);
Vue.component('api-card', ApiCard);
Vue.component('apexchart', VueApexCharts);
