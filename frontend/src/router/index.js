import { createRouter, createWebHistory } from 'vue-router';
import AssetsList from '../views/AssetsList.vue';
import AssetDetail from '../views/AssetDetail.vue';

const routes = [
  { path: '/', redirect: '/assets/laptop' },
  { path: '/assets/:type', name: 'assets-by-type', component: AssetsList, props: true },
  { path: '/assets/:type/:id', name: 'asset-detail', component: AssetDetail, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
