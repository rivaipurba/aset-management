<template>
  <div>
    <!-- Desktop Table View -->
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold">
            <th class="px-6 py-4">#</th>
            <th class="px-6 py-4">Nama Aset</th>
            <th class="px-6 py-4">Seri</th>
            <th class="px-6 py-4">Pembuat</th>
            <th class="px-6 py-4">Pemilik</th>
            <th class="px-6 py-4">Lokasi</th>
            <th class="px-6 py-4">Status</th>
            <th class="px-6 py-4 text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-700 bg-white dark:bg-slate-800">
          <tr 
            v-for="(a, index) in assets" 
            :key="a.id"
            class="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors"
          >
            <td class="px-6 py-4 text-sm text-slate-500 dark:text-slate-400">{{ index + 1 }}</td>
            <td class="px-6 py-4">
              <div class="font-medium text-slate-800 dark:text-slate-100">{{ a.name }}</div>
            </td>
            <td class="px-6 py-4 text-sm text-slate-600 dark:text-slate-300 font-mono">{{ a.serial_number }}</td>
            <td class="px-6 py-4 text-sm text-slate-600 dark:text-slate-300">{{ a.maker }}</td>
            <td class="px-6 py-4 text-sm text-slate-600 dark:text-slate-300">{{ a.owner }}</td>
            <td class="px-6 py-4 text-sm text-slate-600 dark:text-slate-300">
              <div class="flex items-center gap-1.5">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ a.location }}
              </div>
            </td>
            <td class="px-6 py-4">
              <span :class="['px-2.5 py-0.5 rounded-full text-xs font-medium border', statusColor(a.status)]">
                {{ humanStatus(a.status) }}
              </span>
            </td>
            <td class="px-6 py-4 text-center relative">
              <button @click.stop="toggleDropdown($event, a)" class="p-2 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
              </button>
            </td>
          </tr>
          <tr v-if="assets.length === 0">
            <td colspan="8" class="px-6 py-12 text-center text-slate-500 dark:text-slate-400">
              <div class="flex flex-col items-center gap-2">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-slate-300 dark:text-slate-600"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                <p>Tidak ada data aset ditemukan.</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile Card View -->
    <div class="md:hidden space-y-4 p-4">
      <div v-for="a in assets" :key="a.id" class="bg-white dark:bg-slate-800 p-5 border border-slate-200 dark:border-slate-700 rounded-xl shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <div>
            <div class="font-semibold text-slate-800 dark:text-white text-lg">{{ a.name }}</div>
            <div class="text-sm text-slate-500 dark:text-slate-400 font-mono mt-0.5">{{ a.serial_number }}</div>
          </div>
          <button @click.stop="toggleDropdown($event, a)" class="p-2 -mr-2 -mt-2 rounded-lg text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
          </button>
        </div>
        
        <div class="space-y-2 text-sm">
          <div class="flex justify-between py-1 border-b border-slate-100 dark:border-slate-700/50">
            <span class="text-slate-500 dark:text-slate-400">Lokasi</span>
            <span class="font-medium text-slate-700 dark:text-slate-200">{{ a.location || '-' }}</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-100 dark:border-slate-700/50">
            <span class="text-slate-500 dark:text-slate-400">Pemilik</span>
            <span class="font-medium text-slate-700 dark:text-slate-200">{{ a.owner || '-' }}</span>
          </div>
          <div class="flex justify-between items-center pt-1">
            <span class="text-slate-500 dark:text-slate-400">Status</span>
            <span :class="['px-2.5 py-0.5 rounded-full text-xs font-medium border', statusColor(a.status)]">
              {{ humanStatus(a.status) }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-if="assets.length === 0" class="text-center py-12 text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
        <p>Tidak ada data aset ditemukan.</p>
      </div>
    </div>
  </div>

  <Teleport to="body">
    <div 
      v-if="activeAsset" 
      class="fixed inset-0 z-40" 
      @click="closeDropdown"
    ></div>
    <div 
      v-if="activeAsset" 
      class="absolute w-48 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl z-50 overflow-hidden ring-1 ring-black/5"
      :style="{ top: `${dropdownPos.top}px`, left: `${dropdownPos.left}px` }"
    >
      <div class="py-1">
        <a href="#" @click.prevent="$emit('view', activeAsset); closeDropdown()" class="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
          <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          Lihat Detail
        </a>
        <a href="#" @click.prevent="$emit('edit', activeAsset); closeDropdown()" class="flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
          <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          Ubah Data
        </a>
        <div class="h-px bg-slate-100 dark:bg-slate-700 my-1"></div>
        <a href="#" @click.prevent="$emit('delete', activeAsset); closeDropdown()" class="flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors">
          <svg class="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          Hapus Aset
        </a>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  assets: Array,
  type: String
});

const activeAsset = ref(null);
const dropdownPos = reactive({ top: 0, left: 0 });

const toggleDropdown = (event, asset) => {
  if (activeAsset.value && activeAsset.value.id === asset.id) {
    activeAsset.value = null;
    return;
  }

  const rect = event.currentTarget.getBoundingClientRect();
  const dropdownHeight = 160; 
  const dropdownWidth = 192; // w-48

  // Set vertical position
  if (rect.bottom + dropdownHeight > window.innerHeight) {
    dropdownPos.top = rect.top - dropdownHeight + window.scrollY;
  } else {
    dropdownPos.top = rect.bottom + window.scrollY;
  }

  // Set horizontal position
  if (rect.right - dropdownWidth < 0) {
     dropdownPos.left = rect.left + window.scrollX;
  } else {
     dropdownPos.left = rect.right - dropdownWidth + window.scrollX;
  }
  
  activeAsset.value = asset;
};

const closeDropdown = () => {
  activeAsset.value = null;
};

// Handle scroll to close dropdown
const handleScroll = () => {
  if (activeAsset.value) closeDropdown();
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll, true);
  window.addEventListener('resize', closeDropdown);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll, true);
  window.removeEventListener('resize', closeDropdown);
});


const humanStatus = (s) => {
  switch (s) {
    case "available": return "Tersedia";
    case "in_use": return "Sedang dipakai";
    case "maintenance": return "Perawatan";
    case "retired": return "Pensiun";
    default: return s;
  }
};

const statusColor = (s) => {
  switch (s) {
    case 'available': return 'bg-emerald-100 text-emerald-700 border-emerald-200 dark:bg-emerald-900/30 dark:text-emerald-400 dark:border-emerald-800';
    case 'in_use': return 'bg-blue-100 text-blue-700 border-blue-200 dark:bg-blue-900/30 dark:text-blue-400 dark:border-blue-800';
    case 'maintenance': return 'bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-900/30 dark:text-amber-400 dark:border-amber-800';
    case 'retired': return 'bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700';
    default: return 'bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700';
  }
};
</script>
