<template>
  <div class="min-h-[80vh] space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 dark:text-white tracking-tight">
          Aset — {{ currentType.toUpperCase() }}
        </h1>
        <p class="text-slate-500 dark:text-slate-400 mt-1">
          Kelola daftar aset {{ currentType }} Anda.
        </p>
      </div>

      <div class="flex flex-col sm:flex-row items-center gap-3">
        <div class="relative w-full sm:w-64">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-slate-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </div>
          <input 
            v-model="q"
            placeholder="Cari aset..."
            class="pl-10 pr-4 py-2.5 border border-slate-300 dark:border-slate-600 rounded-lg w-full bg-slate-50 dark:bg-slate-700/50 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
          />
        </div>

        <button @click="openCreate" class="w-full sm:w-auto flex items-center justify-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg shadow-sm transition-colors">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Tambah
        </button>
      </div>
    </div>

    <!-- Table Container -->
    <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-sm overflow-hidden">
      <AssetTable 
        :assets="assets"
        :type="currentType"
        @edit="openEdit"
        @delete="removeAsset"
        @view="goToDetail"
      />
      
      <!-- Pagination -->
      <div class="flex flex-col sm:flex-row items-center justify-between px-6 py-4 border-t border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 gap-4">
        <div class="text-sm text-slate-500 dark:text-slate-400">
          Menampilkan <span class="font-medium text-slate-800 dark:text-slate-200">{{ assets.length }}</span> dari <span class="font-medium text-slate-800 dark:text-slate-200">{{ count }}</span> data
        </div>

        <div class="flex gap-2">
          <button 
            @click="prev" 
            :disabled="page <= 1"
            class="px-3 py-1.5 border border-slate-300 dark:border-slate-600 rounded-md text-sm font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-700 hover:bg-slate-50 dark:hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Sebelumnya
          </button>

          <button 
            @click="next"
            :disabled="!nextPage"
            class="px-3 py-1.5 border border-slate-300 dark:border-slate-600 rounded-md text-sm font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-700 hover:bg-slate-50 dark:hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Berikutnya
          </button>
        </div>
      </div>
    </div>

    <!-- Form -->
    <AssetForm 
      v-if="showForm"
      :type="currentType"
      :initial="editing"
      @close="closeForm"
      @saved="onSaved"
    />

    <!-- Delete Confirmation -->
    <ConfirmDialog
      v-if="showDeleteConfirm"
      title="Hapus Aset"
      :message="`Apakah Anda yakin ingin menghapus aset '${assetToDelete?.name}'? Tindakan ini tidak dapat dibatalkan.`"
      @confirm="executeDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import AssetTable from '../components/AssetTable.vue';
import AssetForm from '../components/AssetForm.vue';
import { toastSuccess, toastError } from '../utils/toast';
import ConfirmDialog from '../components/ConfirmDialog.vue';

const route = useRoute();
const router = useRouter();

const assets = ref([]);
const q = ref("");

const showForm = ref(false);
const editing = ref(null);

// Delete confirmation state
const showDeleteConfirm = ref(false);
const assetToDelete = ref(null);

// pagination
const page = ref(1);
const nextPage = ref(null);
const count = ref(0);
const pageSize = 25;

const currentType = computed(() => {
  return route.params.type || 'laptop';
});

const totalPages = computed(() => Math.max(1, Math.ceil(count.value / pageSize)));

async function fetchAssets() {
  try {
    const res = await api.listAssets({
      type: currentType.value,
      search: q.value || undefined,
      page: page.value,
    });
    assets.value = res.data.results || [];
    nextPage.value = res.data.next;
    count.value = res.data.count || 0;
  } catch (err) {
    console.error(err);
    toastError('Gagal memuat data aset');
  }
}

function openCreate() { editing.value = null; showForm.value = true; }
function openEdit(a) { editing.value = a; showForm.value = true; }
function closeForm() { showForm.value = false; editing.value = null; }

function onSaved() {
  closeForm();
  fetchAssets();
}

// --- Delete Logic ---
function removeAsset(asset) {
  assetToDelete.value = asset;
  showDeleteConfirm.value = true;
}

function cancelDelete() {
  showDeleteConfirm.value = false;
  assetToDelete.value = null;
}

async function executeDelete() {
  if (!assetToDelete.value) return;
  try {
    await api.deleteAsset(assetToDelete.value.id);
    toastSuccess('Aset berhasil dihapus');
    fetchAssets();
  } catch {
    toastError('Gagal menghapus aset');
  } finally {
    cancelDelete();
  }
}
// --- End Delete Logic ---

function next() { if (nextPage.value) { page.value++; fetchAssets(); } }
function prev() { if (page.value > 1) { page.value--; fetchAssets(); } }

function goToDetail(a) {
  router.push({ name: 'asset-detail', params: { type: currentType.value, id: a.id } });
}

// --- Watchers ---
let debounceTimer = null;
watch(q, () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    page.value = 1; // Reset to first page on new search
    fetchAssets();
  }, 500); // 500ms debounce
});

watch(() => route.params.type, () => {
  page.value = 1;
  q.value = '';
  fetchAssets();
});

onMounted(fetchAssets);
</script>
