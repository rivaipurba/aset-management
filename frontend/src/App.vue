<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow rounded-lg px-4 py-3 mb-4 mx-4 mt-4">
      <div class="flex items-center justify-between">
        <div class="flex flex-wrap gap-2">
          <RouterLink
            v-for="item in menu"
            :key="item.to"
            :to="item.to"
            class="px-3 py-1 rounded border text-sm"
            :class="isActive(item.to) ? 'bg-indigo-600 text-white border-transparent' : 'text-gray-700'"
            >{{ item.label }}</RouterLink>
        </div>

        <div class="text-sm text-gray-500">Manajemen Aset TI</div>
      </div>
    </nav>

    <main class="mx-4 mb-8">
      <router-view />
    </main>

    <!-- Toast di root supaya dapat dipanggil dari mana saja -->
    <Toast />
  </div>
</template>

<script setup>
import { useRouter, useRoute, RouterLink } from 'vue-router';
import Toast from './components/Toast.vue';

const router = useRouter();
const route = useRoute();

const menu = [
  { to: '/assets/laptop', label: 'Laptop' },
  { to: '/assets/pc', label: 'PC' },
  { to: '/assets/printer', label: 'Printer' },
  { to: '/assets/monitor', label: 'Monitor' },
  { to: '/assets/scanner', label: 'Scanner' },
];

function isActive(path) {
  // simple active check: startsWith so '/assets/laptop/1' tetap memberi active pada /assets/laptop
  return route.path.startsWith(path);
}
</script>

<style>
/* optional small tweak */
#app { font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
</style>
