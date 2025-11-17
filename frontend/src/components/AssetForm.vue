<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-30 p-4">
    <div class="bg-white rounded-lg p-6 w-full max-w-xl">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-medium">{{ initial ? 'Ubah' : 'Tambah' }} {{ typeLabel }}</h3>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">Tutup</button>
      </div>

      <form @submit.prevent="onSubmit" class="space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="block text-sm text-gray-600">Nama</label>
            <input v-model="form.name" required class="mt-1 block w-full border rounded px-2 py-2" />
          </div>

          <div>
            <label class="block text-sm text-gray-600">Nomor Seri</label>
            <input v-model="form.serial_number" class="mt-1 block w-full border rounded px-2 py-2" />
          </div>

          <div>
            <label class="block text-sm text-gray-600">Pembuat</label>
            <input v-model="form.maker" class="mt-1 block w-full border rounded px-2 py-2" />
          </div>

          <div>
            <label class="block text-sm text-gray-600">Pemilik</label>
            <input v-model="form.owner" class="mt-1 block w-full border rounded px-2 py-2" />
          </div>

          <div>
            <label class="block text-sm text-gray-600">Lokasi</label>
            <input v-model="form.location" class="mt-1 block w-full border rounded px-2 py-2" />
          </div>

          <div>
            <label class="block text-sm text-gray-600">Status</label>
            <select v-model="form.status" class="mt-1 block w-full border rounded px-2 py-2">
              <option value="available">Tersedia</option>
              <option value="in_use">Sedang dipakai</option>
              <option value="maintenance">Perawatan</option>
              <option value="retired">Pensiun</option>
            </select>
          </div>

          <div>
            <label class="block text-sm text-gray-600">Kondisi</label>
            <select v-model="form.condition" class="mt-1 block w-full border rounded px-2 py-2">
              <option value="good">Baik</option>
              <option value="fair">Cukup</option>
              <option value="bad">Buruk</option>
            </select>
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm text-gray-600">Catatan</label>
            <textarea v-model="form.notes" class="mt-1 block w-full border rounded px-2 py-2"></textarea>
          </div>
        </div>

        <!-- spesifikasi jenis -->
        <div v-if="isComputer" class="mt-2">
          <h4 class="font-medium text-gray-700 mb-2">Spesifikasi Komputer</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input v-model="form.computer_spec.ram" placeholder="RAM (contoh: 8GB)" class="border rounded px-2 py-2" />
            <input v-model="form.computer_spec.storage" placeholder="Penyimpanan (contoh: 256GB SSD)" class="border rounded px-2 py-2" />
            <input v-model="form.computer_spec.processor" placeholder="Prosesor" class="border rounded px-2 py-2" />
            <input v-model="form.computer_spec.os" placeholder="Sistem Operasi" class="border rounded px-2 py-2" />
          </div>
        </div>

        <div v-if="isPrinter" class="mt-2">
          <label class="block text-sm text-gray-600">Berwarna?</label>
          <select v-model="printerIsColorModel" class="mt-1 block border rounded px-2 py-2">
            <option :value="true">Ya</option>
            <option :value="false">Tidak</option>
          </select>
        </div>

        <div v-if="isMonitor" class="mt-2">
          <label class="block text-sm text-gray-600">Ukuran (inch)</label>
          <input v-model="form.monitor_spec.size_inch" class="mt-1 block w-full border rounded px-2 py-2" />
        </div>

        <div v-if="isScanner" class="mt-2 grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="block text-sm text-gray-600">DPI</label>
            <input v-model.number="form.scanner_spec.dpi" type="number" class="mt-1 block w-full border rounded px-2 py-2" />
          </div>
          <div>
            <label class="block text-sm text-gray-600">Jenis Koneksi</label>
            <input v-model="form.scanner_spec.connection_type" class="mt-1 block w-full border rounded px-2 py-2" />
          </div>
        </div>

        <div class="flex gap-2 justify-end mt-4">
          <button type="button" @click="$emit('close')" class="px-3 py-2 border rounded">Batal</button>
          <button type="submit" class="px-3 py-2 bg-green-600 text-white rounded">Simpan</button>
        </div>
      </form>
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
