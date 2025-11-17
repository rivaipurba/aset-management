<template>
  <div class="bg-white dark:bg-slate-800 shadow rounded-lg p-6 text-slate-800 dark:text-slate-100">

    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
      <h1 class="text-xl font-semibold">
        Aset — {{ currentType.toUpperCase() }}
      </h1>

      <div class="flex items-center gap-2">
        <input 
          v-model="q"
          @keyup.enter="fetchAssets"
          placeholder="Cari nama / seri / pembuat / pemilik"
          class="px-3 py-2 border rounded-lg w-56 md:w-72 dark:bg-slate-700 dark:border-slate-600"
        />

        <button @click="fetchAssets" class="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-500">
          Cari
        </button>

        <button @click="openCreate" class="px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-500">
          + Tambah
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto border border-slate-200 dark:border-slate-700 rounded-lg">
      <AssetTable 
        :assets="assets"
        :type="currentType"
        @edit="openEdit"
        @delete="removeAsset"
        @view="goToDetail"
      />
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between mt-4 text-sm text-slate-600 dark:text-slate-300">
      <div class="flex gap-2">
        <button 
          @click="prev" 
          :disabled="page <= 1"
          class="px-3 py-1 border rounded disabled:opacity-40 dark:border-slate-600"
        >
          Sebelumnya
        </button>

        <button 
          @click="next"
          :disabled="!nextPage"
          class="px-3 py-1 border rounded disabled:opacity-40 dark:border-slate-600"
        >
          Berikutnya
        </button>
      </div>

      <div>
        Halaman {{ page }} / {{ totalPages }} • {{ count }} total  
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import AssetTable from '../components/AssetTable.vue';
import AssetForm from '../components/AssetForm.vue';

const route = useRoute();
const router = useRouter();

const assets = ref([]);
const q = ref("");

const showForm = ref(false);
const editing = ref(null);

// pagination
const page = ref(1);
const nextPage = ref(null);
const count = ref(0);
const pageSize = 25;

const currentType = computed(() => {
  // route.params.type dari URL; fallback ke 'laptop'
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
    window.dispatchEvent(new CustomEvent('toast', {
      detail: { message: 'Gagal memuat data aset', type: 'error' }
    }));
  }
}

function openCreate() { editing.value = null; showForm.value = true; }
function openEdit(a) { editing.value = a; showForm.value = true; }
function closeForm() { showForm.value = false; editing.value = null; }

function onSaved() {
  closeForm();
  fetchAssets();
}

async function removeAsset(asset) {
  if (!confirm(`Hapus aset "${asset.name}"?`)) return;

  try {
    await api.deleteAsset(asset.id);
    fetchAssets();
    window.dispatchEvent(new CustomEvent('toast', {
      detail: { message: 'Aset berhasil dihapus', type: 'success' }
    }));
  } catch {
    window.dispatchEvent(new CustomEvent('toast', {
      detail: { message: 'Gagal menghapus aset', type: 'error' }
    }));
  }
}

function next() { if (nextPage.value) { page.value++; fetchAssets(); } }
function prev() { if (page.value > 1) { page.value--; fetchAssets(); } }

function goToDetail(a) {
  router.push({ name: 'asset-detail', params: { type: currentType.value, id: a.id } });
}

// Watch route.params.type — refetch when it changes (so sidebar clicks act)
watch(() => route.params.type, (newVal, oldVal) => {
  page.value = 1;
  q.value = '';
  fetchAssets();
});

// initial load
onMounted(fetchAssets);
</script>
