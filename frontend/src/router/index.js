// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import AssetsList from '@/views/AssetsList.vue';
import AssetDetail from '@/views/AssetDetail.vue';

// jika kamu ingin page Dashboard, tambahkan file view dan uncomment
import Dashboard from '@/views/Dashboard.vue';

const routes = [
  { path: '/', redirect: '/assets/laptop' },

  // dashboard optional
  { path: '/dashboard', name: 'dashboard', component: Dashboard },

  {
    path: '/assets/:type',
    name: 'assets-list',
    component: AssetsList,
    props: true
  },

  {
    path: '/asset/:type/:id',
    name: 'asset-detail',
    component: AssetDetail,
    props: true
  },

  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
