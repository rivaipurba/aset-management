<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="$emit('close')"></div>

    <!-- Modal Panel -->
    <div class="relative bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden transform transition-all">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between bg-slate-50/50 dark:bg-slate-800/50">
        <h3 class="text-lg font-semibold text-slate-800 dark:text-white">
          {{ initial ? 'Ubah Data' : 'Tambah Aset Baru' }} — {{ typeLabel }}
        </h3>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-500 dark:hover:text-slate-300 transition-colors p-1 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <!-- Scrollable Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <form @submit.prevent="onSubmit" id="asset-form" class="space-y-6">
          <!-- General Info Section -->
          <div class="space-y-4">
            <h4 class="text-sm font-medium text-slate-900 dark:text-slate-200 flex items-center gap-2 pb-2 border-b border-slate-100 dark:border-slate-700/50">
              <svg class="w-4 h-4 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
              Informasi Umum
            </h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Nama Aset <span class="text-red-500">*</span></label>
                <input v-model="form.name" required class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: Laptop Dell XPS 15" />
              </div>

              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Nomor Seri</label>
                <input v-model="form.serial_number" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="SN-12345678" />
              </div>

              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Pembuat (Merk)</label>
                <input v-model="form.maker" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: Dell, HP, Lenovo" />
              </div>

              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Pemilik</label>
                <input v-model="form.owner" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Nama pengguna atau departemen" />
              </div>

              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Lokasi</label>
                <input v-model="form.location" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: Lantai 2, Ruang Server" />
              </div>

              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Status</label>
                <select v-model="form.status" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3">
                  <option value="available">Tersedia</option>
                  <option value="in_use">Sedang dipakai</option>
                  <option value="maintenance">Perawatan</option>
                  <option value="retired">Pensiun</option>
                </select>
              </div>

              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Kondisi</label>
                <select v-model="form.condition" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3">
                  <option value="good">Baik</option>
                  <option value="fair">Cukup</option>
                  <option value="bad">Buruk</option>
                </select>
              </div>

              <div class="md:col-span-2 space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Catatan</label>
                <textarea v-model="form.notes" rows="3" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Tambahkan catatan jika perlu..."></textarea>
              </div>
            </div>
          </div>

          <!-- Specifications Section -->
          <div v-if="isComputer || isPrinter || isMonitor || isScanner" class="space-y-4 pt-2">
            <h4 class="text-sm font-medium text-slate-900 dark:text-slate-200 flex items-center gap-2 pb-2 border-b border-slate-100 dark:border-slate-700/50">
              <svg class="w-4 h-4 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20"></path><path d="M2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6"></path><path d="M12 12V8a2 2 0 0 0-2-2H6"></path></svg>
              Spesifikasi Teknis
            </h4>

            <!-- Computer Specs -->
            <div v-if="isComputer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">RAM</label>
                <input v-model="form.computer_spec.ram" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: 16GB DDR4" />
              </div>
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Penyimpanan</label>
                <input v-model="form.computer_spec.storage" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: 512GB NVMe SSD" />
              </div>
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Prosesor</label>
                <input v-model="form.computer_spec.processor" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: Intel Core i7-12700H" />
              </div>
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Sistem Operasi</label>
                <input v-model="form.computer_spec.os" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: Windows 11 Pro" />
              </div>
            </div>

            <!-- Printer Specs -->
            <div v-if="isPrinter" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Tipe Cetak</label>
                <select v-model="printerIsColorModel" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3">
                  <option :value="true">Berwarna (Color)</option>
                  <option :value="false">Hitam Putih (Monochrome)</option>
                </select>
              </div>
            </div>

            <!-- Monitor Specs -->
            <div v-if="isMonitor" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Ukuran Layar (Inch)</label>
                <input v-model="form.monitor_spec.size_inch" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: 24" />
              </div>
            </div>

            <!-- Scanner Specs -->
            <div v-if="isScanner" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Resolusi (DPI)</label>
                <input v-model.number="form.scanner_spec.dpi" type="number" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: 1200" />
              </div>
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Jenis Koneksi</label>
                <input v-model="form.scanner_spec.connection_type" class="block w-full rounded-lg border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700/50 text-slate-900 dark:text-slate-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3" placeholder="Contoh: USB, WiFi" />
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 border-t border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 flex justify-end gap-3">
        <button type="button" @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors">
          Batal
        </button>
        <button type="submit" form="asset-form" class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-sm transition-colors">
          Simpan
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed, ref, watch } from 'vue';
import api from '../services/api';
import { toastSuccess, toastError } from '../utils/toast';

export default {
  props: { type: String, initial: Object },
  setup(props, { emit }) {
    const isComputer = computed(() => ['laptop', 'pc'].includes(props.type));
    const isPrinter = computed(() => props.type === 'printer');
    const isMonitor = computed(() => props.type === 'monitor');
    const isScanner = computed(() => props.type === 'scanner');

    const form = reactive({
      asset_type: props.initial?.asset_type || ({ laptop:1, pc:2, printer:3, scanner:4, monitor:5 }[props.type]),
      name: props.initial?.name || '',
      serial_number: props.initial?.serial_number || '',
      maker: props.initial?.maker || '',
      owner: props.initial?.owner || '',
      location: props.initial?.location || '',
      status: props.initial?.status || 'available',
      condition: props.initial?.condition || 'good',
      notes: props.initial?.notes || '',
      computer_spec: Object.assign({ ram:'', storage:'', processor:'', os:'' }, props.initial?.computer_spec || {}),
      printer_spec: Object.assign({ is_color:false }, props.initial?.printer_spec || {}),
      monitor_spec: Object.assign({ size_inch:'' }, props.initial?.monitor_spec || {}),
      scanner_spec: Object.assign({ dpi:null, connection_type:'' }, props.initial?.scanner_spec || {})
    });

    const printerIsColorModel = ref(Boolean(form.printer_spec.is_color));
    watch(printerIsColorModel, (v) => { form.printer_spec.is_color = v; }, { immediate: true });

    watch(() => props.initial, (n) => {
      if (!n) return;
      form.asset_type = n.asset_type || form.asset_type;
      form.name = n.name || '';
      form.serial_number = n.serial_number || '';
      form.maker = n.maker || '';
      form.owner = n.owner || '';
      form.location = n.location || '';
      form.status = n.status || form.status;
      form.condition = n.condition || form.condition;
      form.notes = n.notes || '';
      form.computer_spec = Object.assign({ ram:'', storage:'', processor:'', os:'' }, n.computer_spec || {});
      form.printer_spec = Object.assign({ is_color:false }, n.printer_spec || {});
      form.monitor_spec = Object.assign({ size_inch:'' }, n.monitor_spec || {});
      form.scanner_spec = Object.assign({ dpi:null, connection_type:'' }, n.scanner_spec || {});
      printerIsColorModel.value = Boolean(form.printer_spec.is_color);
    }, { immediate: true });

    const typeLabel = computed(() => props.type ? props.type.toUpperCase() : 'Aset');

    async function onSubmit() {
      try {
        const payload = JSON.parse(JSON.stringify(form));
        if (isPrinter.value) {
          if (typeof payload.printer_spec?.is_color === 'string') {
            payload.printer_spec.is_color = payload.printer_spec.is_color === 'true' || payload.printer_spec.is_color === '1';
          }
        }
        if (!isComputer.value) delete payload.computer_spec;
        if (!isPrinter.value) delete payload.printer_spec;
        if (!isMonitor.value) delete payload.monitor_spec;
        if (!isScanner.value) delete payload.scanner_spec;

        if (props.initial && props.initial.id) {
          await api.updateAsset(props.initial.id, payload);
          toastSuccess('Aset berhasil diperbarui');
        } else {
          await api.createAsset(payload);
          toastSuccess('Aset berhasil ditambahkan');
        }
        emit('saved');
      } catch (err) {
        console.error('onSubmit error', err);
        const message = err?.response?.data ? JSON.stringify(err.response.data) : (err.message || 'Terjadi kesalahan');
        toastError('Gagal menyimpan aset: ' + message);
      }
    }

    return {
      form, isComputer, isPrinter, isMonitor, isScanner,
      printerIsColorModel, typeLabel, onSubmit
    };
  }
};
</script>
