<template>
  <div class="min-h-[80vh] space-y-6">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
      <div class="flex items-start gap-4">
        <div class="p-3 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-300">
          <!-- Icon based on type -->
          <span v-html="getIconForType(type)" class="flex items-center justify-center w-8 h-8"></span>
        </div>
        <div>
          <div class="flex items-center gap-3 mb-1">
            <h1 class="text-2xl font-bold text-slate-800 dark:text-white tracking-tight">{{ asset?.name || '—' }}</h1>
            <span :class="['px-2.5 py-0.5 rounded-full text-xs font-medium border', statusColor(asset?.status)]">
              {{ humanStatus(asset?.status) }}
            </span>
          </div>
          <div class="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
            <span class="flex items-center gap-1">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
              SN: <span class="font-mono text-slate-700 dark:text-slate-300">{{ asset?.serial_number || '-' }}</span>
            </span>
            <span class="hidden sm:inline text-slate-300 dark:text-slate-600">|</span>
            <span class="flex items-center gap-1">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              Update: {{ asset?.updated_at ? new Date(asset.updated_at).toLocaleDateString() : '-' }}
            </span>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button @click="goEdit" class="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-600 transition-colors shadow-sm">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
          Ubah
        </button>
        <button @click="doDelete" class="flex items-center gap-2 px-4 py-2 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors shadow-sm">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
          Hapus
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: General Info -->
      <div class="lg:col-span-2 space-y-6">
        <!-- General Info Card -->
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50">
            <h3 class="font-semibold text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-500"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
              Informasi Umum
            </h3>
          </div>
          <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-1">
              <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Pembuat (Merk)</div>
              <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.maker || '-' }}</div>
            </div>
            <div class="space-y-1">
              <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Pemilik</div>
              <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.owner || '-' }}</div>
            </div>
            <div class="space-y-1">
              <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Lokasi</div>
              <div class="text-slate-800 dark:text-slate-100 font-medium flex items-center gap-1">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-slate-400"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                {{ asset?.location || '-' }}
              </div>
            </div>
            <div class="space-y-1 md:col-span-2">
              <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Catatan</div>
              <div class="text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border border-slate-100 dark:border-slate-700/50 text-sm leading-relaxed">
                {{ asset?.notes || 'Tidak ada catatan tambahan.' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Specs Card -->
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50">
            <h3 class="font-semibold text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-500"><path d="M2 12h20"></path><path d="M2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6"></path><path d="M12 12V8a2 2 0 0 0-2-2H6"></path></svg>
              Spesifikasi Teknis
            </h3>
          </div>
          <div class="p-6">
            <div v-if="isComputer" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Prosesor</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.computer_spec?.processor || '-' }}</div>
              </div>
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">RAM</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.computer_spec?.ram || '-' }}</div>
              </div>
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Penyimpanan</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.computer_spec?.storage || '-' }}</div>
              </div>
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Sistem Operasi</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.computer_spec?.os || '-' }}</div>
              </div>
            </div>

            <div v-else-if="isPrinter" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Tipe Cetak</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">
                  <span v-if="asset?.printer_spec?.is_color" class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-gradient-to-r from-blue-500 via-green-500 to-red-500"></span>
                    Warna
                  </span>
                  <span v-else class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-slate-800"></span>
                    Hitam Putih
                  </span>
                </div>
              </div>
            </div>

            <div v-else-if="isMonitor" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Ukuran Layar</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.monitor_spec?.size_inch ? asset.monitor_spec.size_inch + ' Inch' : '-' }}</div>
              </div>
            </div>

            <div v-else-if="isScanner" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Resolusi (DPI)</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.scanner_spec?.dpi || '-' }}</div>
              </div>
              <div class="space-y-1">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Konektivitas</div>
                <div class="text-slate-800 dark:text-slate-100 font-medium">{{ asset?.scanner_spec?.connection_type || '-' }}</div>
              </div>
            </div>

            <div v-else class="text-sm text-slate-500 italic">
              Tidak ada spesifikasi khusus untuk jenis aset ini.
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Meta / History (Placeholder) -->
      <div class="space-y-6">
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50">
            <h3 class="font-semibold text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-500"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              Riwayat
            </h3>
          </div>
          <div class="p-6">
            <div class="relative pl-4 border-l-2 border-slate-200 dark:border-slate-700 space-y-6">
              <div class="relative">
                <div class="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-indigo-500 ring-4 ring-white dark:ring-slate-800"></div>
                <div class="text-sm font-medium text-slate-800 dark:text-slate-100">Data Diperbarui</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ asset?.updated_at ? new Date(asset.updated_at).toLocaleString() : 'Belum pernah' }}</div>
              </div>
              <div class="relative">
                <div class="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-slate-300 dark:bg-slate-600 ring-4 ring-white dark:ring-slate-800"></div>
                <div class="text-sm font-medium text-slate-800 dark:text-slate-100">Aset Dibuat</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ asset?.created_at ? new Date(asset.created_at).toLocaleString() : '-' }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Form Modal -->
  <AssetForm 
    v-if="showForm"
    :type="type"
    :initial="editing"
    @close="closeForm"
    @saved="onSaved"
  />

  <!-- Delete Confirmation -->
  <ConfirmDialog
    v-if="showDeleteConfirm"
    title="Hapus Aset"
    :message="`Apakah Anda yakin ingin menghapus aset '${asset?.name}'? Tindakan ini tidak dapat dibatalkan.`"
    @confirm="executeDelete"
    @cancel="cancelDelete"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
import { useRoute, useRouter } from 'vue-router';
import AssetForm from '../components/AssetForm.vue';
import { toastSuccess, toastError } from '../utils/toast';
import ConfirmDialog from '../components/ConfirmDialog.vue';
import { humanStatus, statusColor } from '../utils/assetUtils';

const route = useRoute();
const router = useRouter();
const asset = ref(null);

// Form state
const showForm = ref(false);
const editing = ref(null);

// Delete confirmation state
const showDeleteConfirm = ref(false);

const type = route.params.type || 'laptop';
const id = route.params.id;

const isComputer = computed(() => ['laptop','pc'].includes(type));
const isPrinter = computed(() => type === 'printer');
const isMonitor = computed(() => type === 'monitor');
const isScanner = computed(() => type === 'scanner');

function getIconForType(t) {
  const map = {
    laptop: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="2" y1="20" x2="22" y2="20"></line></svg>`,
    pc: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect><rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>`,
    printer: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>`,
    monitor: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>`,
    scanner: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20"></path><path d="M2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6"></path><path d="M12 12V8a2 2 0 0 0-2-2H6"></path></svg>`
  };
  return map[t] || map.laptop;
}

async function load() {
  try {
    const res = await api.getAsset(id);
    asset.value = res.data;
  } catch (err) {
    console.error(err);
    toastError('Gagal memuat detail aset');
  }
}

function goEdit() {
  editing.value = asset.value;
  showForm.value = true;
}

function closeForm() {
  showForm.value = false;
  editing.value = null;
}

function onSaved() {
  closeForm();
  load(); // Reload data to show changes
}

// --- Delete Logic ---
function doDelete() {
  showDeleteConfirm.value = true;
}

function cancelDelete() {
  showDeleteConfirm.value = false;
}

async function executeDelete() {
  try {
    await api.deleteAsset(id);
    toastSuccess('Aset berhasil dihapus');
    router.push(`/assets/${type}`);
  } catch {
    toastError('Gagal menghapus aset');
  } finally {
    cancelDelete();
  }
}
// --- End Delete Logic ---

onMounted(load);
</script>

<style scoped>
/* Pastikan teks tidak transparan karena style global */
:root, .asset-detail-root {
  color: inherit;
  opacity: 1;
}
</style>
