<template>
  <div class="p-6 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 shadow">
    <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-semibold">{{ asset?.name || '—' }}</h1>
        <div class="text-sm text-slate-600 dark:text-slate-300 mt-1">
          Seri: <span class="font-medium text-slate-800 dark:text-slate-100">{{ asset?.serial_number || '-' }}</span>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <span :class="['px-3 py-1 rounded-full text-sm font-medium', statusColor(asset?.status)]">
          {{ humanStatus(asset?.status) }}
        </span>

        <div class="text-sm text-slate-500 dark:text-slate-300">Diperbarui: <span class="font-medium">{{ asset?.updated_at ? new Date(asset.updated_at).toLocaleString() : '-' }}</span></div>
      </div>
    </div>

    <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="space-y-3">
        <div class="text-xs text-slate-500 dark:text-slate-300">Informasi Umum</div>
        <div class="bg-slate-50 dark:bg-slate-700/40 p-4 rounded">
          <div class="text-sm"><strong>Pembuat:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.maker || '-' }}</span></div>
          <div class="text-sm"><strong>Pemilik:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.owner || '-' }}</span></div>
          <div class="text-sm"><strong>Lokasi:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.location || '-' }}</span></div>
          <div class="text-sm"><strong>Catatan:</strong> <span class="text-slate-700 dark:text-slate-200">{{ asset?.notes || '-' }}</span></div>
        </div>
      </div>

      <div class="space-y-3">
        <div class="text-xs text-slate-500 dark:text-slate-300">Spesifikasi</div>
        <div class="bg-slate-50 dark:bg-slate-700/40 p-4 rounded">
          <template v-if="isComputer">
            <div class="text-sm"><strong>RAM:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.computer_spec?.ram || '-' }}</span></div>
            <div class="text-sm"><strong>Penyimpanan:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.computer_spec?.storage || '-' }}</span></div>
            <div class="text-sm"><strong>Prosesor:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.computer_spec?.processor || '-' }}</span></div>
            <div class="text-sm"><strong>OS:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.computer_spec?.os || '-' }}</span></div>
          </template>

          <template v-else-if="isPrinter">
            <div class="text-sm"><strong>Berwarna:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.printer_spec?.is_color ? 'Ya' : 'Tidak' }}</span></div>
          </template>

          <template v-else-if="isMonitor">
            <div class="text-sm"><strong>Ukuran (inch):</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.monitor_spec?.size_inch || '-' }}</span></div>
          </template>

          <template v-else-if="isScanner">
            <div class="text-sm"><strong>DPI:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.scanner_spec?.dpi || '-' }}</span></div>
            <div class="text-sm"><strong>Koneksi:</strong> <span class="text-slate-800 dark:text-slate-100">{{ asset?.scanner_spec?.connection_type || '-' }}</span></div>
          </template>

          <template v-else>
            <div class="text-sm">-</div>
          </template>
        </div>
      </div>
    </div>

    <div class="mt-6 flex gap-2">
      <button @click="goEdit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500">Ubah</button>
      <button @click="doDelete" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-500">Hapus</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const asset = ref(null);

const type = route.params.type || 'laptop';
const id = route.params.id;

const isComputer = computed(() => ['laptop','pc'].includes(type));
const isPrinter = computed(() => type === 'printer');
const isMonitor = computed(() => type === 'monitor');
const isScanner = computed(() => type === 'scanner');

function humanStatus(s) {
  if (!s) return '-';
  const map = { available: 'Tersedia', in_use: 'Sedang dipakai', maintenance: 'Perawatan', retired: 'Pensiun' };
  return map[s] || s;
}

function statusColor(s) {
  switch (s) {
    case 'available': return 'bg-green-100 text-green-700 dark:bg-green-700/30 dark:text-green-300';
    case 'in_use': return 'bg-blue-100 text-blue-700 dark:bg-blue-700/30 dark:text-blue-300';
    case 'maintenance': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-700/30 dark:text-yellow-300';
    case 'retired': return 'bg-gray-200 text-gray-700 dark:bg-gray-700/30 dark:text-gray-300';
    default: return 'bg-slate-200 text-slate-700 dark:bg-slate-700/40 dark:text-slate-300';
  }
}

async function load() {
  try {
    const res = await api.getAsset(id);
    asset.value = res.data;
  } catch (err) {
    console.error(err);
    window.dispatchEvent(new CustomEvent('toast', { detail: { message: 'Gagal memuat detail aset', type: 'error' } }));
  }
}

function goEdit() {
  router.push({ name: 'assets-list', params: { type, id: asset.value?.id }});
  // atau buka modal edit tergantung implementasimu
}

async function doDelete() {
  if (!confirm('Hapus aset ini?')) return;
  try {
    await api.deleteAsset(id);
    window.dispatchEvent(new CustomEvent('toast', { detail: { message: 'Aset berhasil dihapus', type: 'success' } }));
    router.push(`/assets/${type}`);
  } catch {
    window.dispatchEvent(new CustomEvent('toast', { detail: { message: 'Gagal menghapus aset', type: 'error' } }));
  }
}

onMounted(load);
</script>

<style scoped>
/* Pastikan teks tidak transparan karena style global */
:root, .asset-detail-root {
  color: inherit;
  opacity: 1;
}
</style>
