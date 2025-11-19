<template>
  <div class="min-h-[60vh] space-y-8">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 dark:text-white tracking-tight">Dashboard Aset TI</h1>
        <p class="text-slate-500 dark:text-slate-400 mt-1">
          Ikhtisar real-time inventaris dan status aset.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-800 px-3 py-1.5 rounded-full border dark:border-slate-700 shadow-sm">
          Update terakhir: Baru saja
        </span>
      </div>
    </div>

    <!-- Status Summary -->
    <div v-if="loading" class="text-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
      <span class="text-slate-500">Memuat data...</span>
    </div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card title="Total Aset" :value="totalAssets" :icon="icons.total" />
      <Card title="Tersedia" :value="availableAssets" valueColor="text-emerald-600 dark:text-emerald-400" :icon="icons.available" />
      <Card title="Sedang dipakai" :value="inUseAssets" valueColor="text-blue-600 dark:text-blue-400" :icon="icons.inUse" />
      <Card title="Dalam Perawatan" :value="inMaintenanceAssets" valueColor="text-amber-600 dark:text-amber-400" :icon="icons.maintenance" />
    </div>

    <!-- Asset Type Summary -->
    <div v-if="!loading">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-semibold text-slate-800 dark:text-white">Statistik per Jenis Aset</h2>
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
        <Card v-for="stat in assetTypeStats" :key="stat.code" :title="stat.name" :value="stat.count" :icon="getIconForType(stat.code)" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { toastError } from '../utils/toast';
import Card from '../components/Card.vue';

const loading = ref(true);

// Status stats
const totalAssets = ref(0);
const availableAssets = ref(0);
const inUseAssets = ref(0);
const inMaintenanceAssets = ref(0);

// Type stats
const assetTypeStats = ref([]);
const assetTypes = [
  { code: 'laptop', name: 'Laptop' },
  { code: 'pc', name: 'PC' },
  { code: 'printer', name: 'Printer' },
  { code: 'monitor', name: 'Monitor' },
  { code: 'scanner', name: 'Scanner' },
];

// Icons
const icons = {
  total: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>`,
  available: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`,
  inUse: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
  maintenance: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>`
};

function getIconForType(code) {
  const map = {
    laptop: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="2" y1="20" x2="22" y2="20"></line></svg>`,
    pc: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>`,
    printer: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>`,
    monitor: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>`,
    scanner: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20"></path><path d="M2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6"></path><path d="M12 12V8a2 2 0 0 0-2-2H6"></path></svg>`
  };
  return map[code] || icons.total;
}

async function fetchStats() {
  loading.value = true;
  try {
    const params = { limit: 1 }; // Optimization: we only need the count
    
    // Prepare all promises
    const summaryPromises = [
      api.listAssets(params),
      api.listAssets({ ...params, status: 'available' }),
      api.listAssets({ ...params, status: 'in_use' }),
      api.listAssets({ ...params, status: 'maintenance' })
    ];
    const typePromises = assetTypes.map(type => 
      api.listAssets({ ...params, type: type.code })
    );

    // Fetch all data in parallel
    const allResults = await Promise.all([...summaryPromises, ...typePromises]);

    // Process summary results
    const [totalRes, availableRes, inUseRes, maintenanceRes] = allResults.slice(0, 4);
    totalAssets.value = totalRes.data.count || 0;
    availableAssets.value = availableRes.data.count || 0;
    inUseAssets.value = inUseRes.data.count || 0;
    inMaintenanceAssets.value = maintenanceRes.data.count || 0;

    // Process per-type results
    const typeResults = allResults.slice(4);
    assetTypeStats.value = assetTypes.map((type, index) => ({
      ...type,
      count: typeResults[index].data.count || 0,
    }));

  } catch (err) {
    console.error("Failed to fetch dashboard stats:", err);
    toastError('Gagal memuat statistik dashboard');
  } finally {
    loading.value = false;
  }
}

onMounted(fetchStats);
</script>

<style scoped>
/* untuk memastikan tidak ada opacity yang menurunkan teks */
:root, .dashboard-root {
  color: inherit;
  opacity: 1;
}
</style>
