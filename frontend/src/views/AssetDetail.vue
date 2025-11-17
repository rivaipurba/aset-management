<template>
  <div class="space-y-4">
    <div v-if="!asset" class="text-center py-8">
      <div class="text-gray-600">Memuat data aset…</div>
    </div>

    <div v-else>
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-2xl font-semibold">{{ asset.name }}</h2>
          <p class="text-sm text-gray-600">ID: {{ asset.id }} • Tipe: {{ (asset.asset_type_code || type).toUpperCase() }}</p>
        </div>

        <div class="flex items-center gap-2">
          <button @click="onClickEdit" class="px-3 py-1 bg-blue-600 text-white rounded">Ubah</button>
          <button @click="doDelete" class="px-3 py-1 bg-red-600 text-white rounded">Hapus</button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white border rounded p-4">
          <h3 class="font-medium mb-2">Umum</h3>
          <dl class="grid grid-cols-2 gap-2 text-sm">
            <div><dt class="text-gray-500">Nama</dt><dd>{{ asset.name || '-' }}</dd></div>
            <div><dt class="text-gray-500">Nomor Seri</dt><dd>{{ asset.serial_number || '-' }}</dd></div>
            <div><dt class="text-gray-500">Pembuat</dt><dd>{{ asset.maker || '-' }}</dd></div>
            <div><dt class="text-gray-500">Pemilik</dt><dd>{{ asset.owner || '-' }}</dd></div>
            <div><dt class="text-gray-500">Lokasi</dt><dd>{{ asset.location || '-' }}</dd></div>
            <div><dt class="text-gray-500">Status</dt><dd>{{ humanStatus(asset.status) }}</dd></div>
            <div><dt class="text-gray-500">Kondisi</dt><dd>{{ humanCondition(asset.condition) }}</dd></div>
            <div class="md:col-span-2"><dt class="text-gray-500">Catatan</dt><dd>{{ asset.notes || '-' }}</dd></div>
          </dl>
        </div>

        <div class="bg-white border rounded p-4">
          <h3 class="font-medium mb-2">Spesifikasi</h3>
          <div v-if="isComputer" class="text-sm">
            <div class="grid grid-cols-2 gap-2">
              <div><div class="text-gray-500 text-xs">RAM</div><div>{{ asset.computer_spec?.ram || '-' }}</div></div>
              <div><div class="text-gray-500 text-xs">Penyimpanan</div><div>{{ asset.computer_spec?.storage || '-' }}</div></div>
              <div><div class="text-gray-500 text-xs">Prosesor</div><div>{{ asset.computer_spec?.processor || '-' }}</div></div>
              <div><div class="text-gray-500 text-xs">Sistem Operasi</div><div>{{ asset.computer_spec?.os || '-' }}</div></div>
            </div>
          </div>

          <div v-else-if="isPrinter" class="text-sm">
            <div><div class="text-gray-500 text-xs">Berwarna?</div><div>{{ asset.printer_spec?.is_color ? 'Ya' : 'Tidak' }}</div></div>
          </div>

          <div v-else-if="isMonitor" class="text-sm">
            <div><div class="text-gray-500 text-xs">Ukuran (inch)</div><div>{{ asset.monitor_spec?.size_inch || '-' }}</div></div>
          </div>

          <div v-else-if="isScanner" class="text-sm">
            <div class="grid grid-cols-2 gap-2">
              <div><div class="text-gray-500 text-xs">DPI</div><div>{{ asset.scanner_spec?.dpi || '-' }}</div></div>
              <div><div class="text-gray-500 text-xs">Jenis Koneksi</div><div>{{ asset.scanner_spec?.connection_type || '-' }}</div></div>
            </div>
          </div>

          <div v-else class="text-sm">
            <div v-if="anySpecObject">
              <div v-for="(val, key) in anySpecObject" :key="key" class="mb-1">
                <div class="text-gray-500 text-xs">{{ humanize(key) }}</div>
                <div>{{ val === null ? '-' : String(val) }}</div>
              </div>
            </div>
            <div v-else class="text-sm text-gray-500">Tidak ada spesifikasi</div>
          </div>
        </div>
      </div>

      <!-- Edit modal -->
      <AssetForm v-if="editingAsset" :type="type" :initial="editingAsset" @close="editingAsset=null" @saved="onSavedFromDetail" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';
import AssetForm from '../components/AssetForm.vue';
import { useRoute, useRouter } from 'vue-router';
import { toastSuccess, toastError } from '../utils/toast';

export default {
  components: { AssetForm },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const id = route.params.id;
    const type = route.params.type || 'aset';

    const asset = ref(null);
    const editingAsset = ref(null);

    async function load() {
      try {
        const r = await api.getAsset(id);
        asset.value = r.data;
      } catch (err) {
        console.error('Gagal memuat asset:', err);
        toastError('Gagal memuat data aset');
      }
    }

    function onClickEdit() {
      editingAsset.value = Object.assign({}, asset.value);
    }

    async function doDelete() {
      if (!confirm('Hapus aset ini?')) return;
      try {
        await api.deleteAsset(id);
        toastSuccess('Aset berhasil dihapus');
        router.push(`/assets/${type}`);
      } catch (err) {
        console.error('Gagal menghapus asset:', err);
        toastError('Gagal menghapus aset');
      }
    }

    function onSavedFromDetail() {
      editingAsset.value = null;
      toastSuccess('Aset berhasil diperbarui');
      load();
    }

    const isComputer = computed(() => asset.value && ['laptop', 'pc'].includes((asset.value.asset_type_code || type).toLowerCase()));
    const isPrinter = computed(() => asset.value && (asset.value.asset_type_code || type).toLowerCase() === 'printer');
    const isMonitor = computed(() => asset.value && (asset.value.asset_type_code || type).toLowerCase() === 'monitor');
    const isScanner = computed(() => asset.value && (asset.value.asset_type_code || type).toLowerCase() === 'scanner');

    const anySpecObject = computed(() => {
      return asset.value?.computer_spec || asset.value?.printer_spec || asset.value?.monitor_spec || asset.value?.scanner_spec || null;
    });

    function humanStatus(v) {
      if (!v) return '-';
      const map = {
        available: 'Tersedia',
        in_use: 'Sedang dipakai',
        maintenance: 'Perawatan',
        retired: 'Pensiun'
      };
      return map[v] || v;
    }

    function humanCondition(v) {
      if (!v) return '-';
      const cmap = {
        good: 'Baik',
        fair: 'Cukup',
        bad: 'Buruk'
      };
      return cmap[v] || v;
    }

    function humanize(key) {
      const s = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      if (s.toLowerCase().includes('size')) return s.replace(/Size/i, 'Ukuran');
      if (s.toLowerCase().includes('ram')) return 'RAM';
      if (s.toLowerCase().includes('storage')) return 'Penyimpanan';
      if (s.toLowerCase().includes('processor')) return 'Prosesor';
      if (s.toLowerCase().includes('os')) return 'Sistem Operasi';
      if (s.toLowerCase().includes('is color') || s.toLowerCase().includes('is_color')) return 'Berwarna';
      if (s.toLowerCase().includes('dpi')) return 'DPI';
      if (s.toLowerCase().includes('connection')) return 'Jenis Koneksi';
      return s;
    }

    onMounted(load);

    return {
      asset, editingAsset, onClickEdit, doDelete, onSavedFromDetail, formatDate: (dt) => dt ? new Date(dt).toLocaleString('id-ID') : '-', type,
      isComputer, isPrinter, isMonitor, isScanner, anySpecObject, humanize, humanStatus, humanCondition
    };
  }
};
</script>

<style scoped>
pre { background: #f8fafc; padding: 0.75rem; border-radius: 6px; overflow:auto; }
</style>
