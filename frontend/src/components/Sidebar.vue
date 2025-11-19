<template>
  <aside
    class="bg-white dark:bg-slate-800 border-r dark:border-slate-700 h-screen transition-all duration-200 ease-out"
    :class="{
      'w-64': !collapsed,
      'w-16': collapsed
    }"
  >
    <!-- top area: logo + collapse button -->
    <div class="flex items-center justify-between px-3 py-3 border-b dark:border-slate-700">
      <div @click="toggleCollapse" class="flex items-center gap-2 cursor-pointer">
        <div class="flex items-center justify-center w-9 h-9 rounded bg-indigo-600 text-white">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        </div>
        <div v-if="!collapsed" class="text-sm font-semibold text-slate-700 dark:text-slate-100">Aset TI</div>
      </div>
    </div>

    <!-- menu -->
    <nav class="px-1 py-3">
      <ul class="space-y-1">
        <li v-for="item in menu" :key="item.to">
          <router-link
            :to="item.to"
            class="flex items-center gap-3 px-3 py-2 rounded text-sm hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-150"
            :class="isActive(item.to) ? 'bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-200 font-semibold' : 'text-slate-700 dark:text-slate-200'"
            @click="closeMobile"
          >
            <span class="w-5 h-5 flex items-center justify-center text-lg" v-html="item.icon"></span>
            <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
            <span v-else class="sr-only">{{ item.label }}</span>
            <span v-if="item.badge && !collapsed" class="ml-auto text-xs bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200 px-2 py-0.5 rounded">{{ item.badge }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <div class="mt-auto px-3 py-4 border-t dark:border-slate-700">
      <div v-if="!collapsed" class="text-xs text-slate-500 dark:text-slate-300">Versi: 1.0.0</div>
      <div v-if="!collapsed" class="mt-2">
        <button @click="goToSettings" class="w-full text-left px-3 py-2 rounded hover:bg-slate-100 dark:hover:bg-slate-700 text-sm">Pengaturan</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';

const router = useRouter();
const route = useRoute();

const collapsedKey = 'sidebar_collapsed_v1';
const collapsed = ref(localStorage.getItem(collapsedKey) === '1');

function toggleCollapse() {
  collapsed.value = !collapsed.value;
  localStorage.setItem(collapsedKey, collapsed.value ? '1' : '0');
}

function isActive(path) {
  // active if route path startsWith path
  try {
    return route.path === path || route.path.startsWith(path + '/');
  } catch {
    return false;
  }
}

function goToSettings() {
  router.push('/settings');
}

function closeMobile() {
  // emit event to parent to close mobile drawer if needed
  window.dispatchEvent(new CustomEvent('sidebar:close'));
}

// menu items
const menu = [
  { to: '/dashboard', label: 'Dashboard', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>` },
  { to: '/assets/laptop', label: 'Laptop', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="11" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M2 18h20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>` },
  { to: '/assets/pc', label: 'PC', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="12" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M8 20h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>` },
  { to: '/assets/printer', label: 'Printer', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="6" y="9" width="12" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M6 12h12" stroke="currentColor" stroke-width="1.5"/><rect x="8" y="3" width="8" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>` },
  { to: '/assets/monitor', label: 'Monitor', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="12" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M8 20h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>` },
  { to: '/assets/scanner', label: 'Scanner', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="6" width="18" height="9" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M8 16v2h8v-2" stroke="currentColor" stroke-width="1.5"/></svg>` },
];
</script>

<style scoped>
/* nothing custom besides tailwind classes */
</style>
