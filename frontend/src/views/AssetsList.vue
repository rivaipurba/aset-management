<template>
  <div class="bg-white shadow rounded-lg p-6">
    <header class="mb-4">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <h1 class="text-2xl font-semibold text-gray-700">Aset — {{ type.toUpperCase() }}</h1>

        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full sm:w-auto">

          <!-- SEARCH -->
          <div class="flex gap-2 items-center w-full sm:w-auto">
            <input
              v-model="searchTerm"
              @keyup.enter="doSearchNow"
              placeholder="Cari nama/seri/pembuat/pemilik"
              class="w-full sm:w-72 px-3 py-2 border rounded"
            />
            <button @click="doSearchNow" class="px-3 py-2 bg-indigo-600 text-white rounded">Cari</button>
            <button v-if="searchTerm" @click="clearSearch" class="px-3 py-2 border rounded">Bersihkan</button>
          </div>

          <!-- ADD BUTTON -->
          <div class="flex gap-2 ml-auto">
            <button @click="openCreate" class="px-3 py-2 rounded bg-green-600 text-white hover:bg-green-500">+ Tambah</button>
          </div>

        </div>
      </div>

      <div class="mt-2 text-sm text-gray-500" v-if="isSearching">Mencari…</div>
    </header>

    <!-- Table (pass sorting state & listen sort event) -->
    <AssetTable
      :assets="assets"
      :type="type"
      :sortField="sortField"
      :sortDir="sortDir"
      @edit="openEdit"
      @delete="removeAsset"
      @view="goToDetail"
      @sort="handleSort"
    />

    <!-- Pagination -->
    <div class="flex flex-col sm:flex-row items-center justify-between gap-3 mt-4">
      <div class="flex items-center gap-2">
        <button @click="prev" :disabled="page<=1" class="px-3 py-2 border rounded disabled:opacity-50">Sebelumnya</button>
        <button @click="next" :disabled="!nextPage" class="px-3 py-2 border rounded disabled:opacity-50">Berikutnya</button>
        <div class="text-sm text-gray-600 ml-4">
          Halaman {{ page }}{{ totalPagesText }} • {{ count }} total
        </div>
      </div>

      <div class="text-sm text-gray-600">
        Menampilkan {{ assets.length }} di halaman ini
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

  </div>
</template>

<script>
import { ref, watch, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import AssetTable from '../components/AssetTable.vue';
import AssetForm from '../components/AssetForm.vue';
import { toastSuccess, toastError } from '../utils/toast';

export default {
  props: ['type'],
  components: { AssetTable, AssetForm },

  setup(props) {
    const router = useRouter();

    const assets = ref([]);
    const showForm = ref(false);
    const editing = ref(null);

    // pagination
    const page = ref(1);
    const nextPage = ref(null);
    const prevPage = ref(null);
    const count = ref(0);
    const pageSize = 25;

    const type = computed(() => props.type || 'laptop');
    const totalPages = computed(() => Math.max(1, Math.ceil(count.value / pageSize)));
    const totalPagesText = computed(() => ` / ${totalPages.value}`);

    // search
    const searchTerm = ref('');
    const debouncing = ref(false);
    let debounceTimer = null;
    const isSearching = computed(() => debouncing.value);

    // SORT state
    const sortField = ref(null); // e.g. 'name', 'serial_number'
    const sortDir = ref('asc'); // 'asc' or 'desc'

    function buildOrdering() {
      if (!sortField.value) return '-created_at'; // default ordering
      // backend expects '-field' for descending; create ordering key accordingly
      const prefix = sortDir.value === 'desc' ? '-' : '';
      return `${prefix}${sortField.value}`;
    }

    async function fetchAssets() {
      try {
        const params = {
          type: type.value,
          ordering: buildOrdering(),
          page: page.value,
        };

        if (searchTerm.value.trim() !== '') {
          params.search = searchTerm.value.trim();
        }

        const res = await api.listAssets(params);
        assets.value = res.data.results || [];
        nextPage.value = res.data.next;
        prevPage.value = res.data.previous;
        count.value = res.data.count;
      } catch (err) {
        console.error('fetchAssets error', err);
        toastError('Gagal memuat daftar aset');
      } finally {
        debouncing.value = false;
      }
    }

    // handle header sort event
    function handleSort(field) {
      // jika klik field sama, toggle direction; jika beda, set field & asc
      if (sortField.value === field) {
        sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortField.value = field;
        sortDir.value = 'asc';
      }
      page.value = 1;
      fetchAssets();
    }

    // debounce search
    watch(searchTerm, () => {
      if (debounceTimer) clearTimeout(debounceTimer);
      debouncing.value = true;
      page.value = 1;

      debounceTimer = setTimeout(() => {
        fetchAssets();
      }, 500);
    });

    function doSearchNow() {
      if (debounceTimer) clearTimeout(debounceTimer);
      debouncing.value = false;
      page.value = 1;
      fetchAssets();
    }

    function clearSearch() {
      searchTerm.value = '';
      page.value = 1;
      fetchAssets();
    }

    // CRUD actions
    function openCreate() {
      editing.value = null;
      showForm.value = true;
    }

    function openEdit(asset) {
      editing.value = asset;
      showForm.value = true;
    }

    function closeForm() {
      showForm.value = false;
      editing.value = null;
    }

    function onSaved() {
      closeForm();
      fetchAssets();
    }

    async function removeAsset(asset) {
      if (!confirm(`Hapus aset "${asset.name}"?`)) return;

      try {
        await api.deleteAsset(asset.id);
        toastSuccess('Aset berhasil dihapus');
        fetchAssets();
      } catch (err) {
        console.error(err);
        toastError('Gagal menghapus aset');
      }
    }

    function next() {
      if (!nextPage.value) return;
      page.value++;
      fetchAssets();
    }

    function prev() {
      if (page.value <= 1) return;
      page.value--;
      fetchAssets();
    }

    function goToDetail(asset) {
      router.push({
        name: 'asset-detail',
        params: { type: type.value, id: asset.id }
      });
    }

    // reload when type changes
    watch(() => props.type, () => {
      page.value = 1;
      sortField.value = null;
      sortDir.value = 'asc';
      fetchAssets();
    }, { immediate: true });

    onMounted(fetchAssets);

    return {
      assets, type,
      showForm, editing,
      page, nextPage, prevPage, count,
      totalPagesText,
      searchTerm, isSearching,

      fetchAssets,
      openCreate, openEdit, closeForm, onSaved,
      removeAsset,
      next, prev,
      goToDetail,

      doSearchNow, clearSearch,

      // expose sort to table
      sortField, sortDir, handleSort
    };
  }
};
</script>
