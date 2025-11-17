<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-30 p-4">
    <div class="bg-white rounded-lg p-5 w-full max-w-md">
      <h3 class="text-lg font-medium mb-3">Pindah: {{ asset.name }}</h3>
      <form @submit.prevent="doMove" class="space-y-3">
        <div>
          <label class="text-sm text-gray-600">Dari</label>
          <input :value="asset.location" disabled class="mt-1 w-full border rounded px-2 py-2 bg-gray-100" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Ke (wajib)</label>
          <input v-model="to_location" required class="mt-1 w-full border rounded px-2 py-2" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Dilakukan oleh</label>
          <input v-model="performed_by" class="mt-1 w-full border rounded px-2 py-2" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Catatan</label>
          <textarea v-model="note" class="mt-1 w-full border rounded px-2 py-2"></textarea>
        </div>
        <div class="flex justify-end gap-2">
          <button type="button" @click="$emit('close')" class="px-3 py-2 border rounded">Batal</button>
          <button type="submit" class="px-3 py-2 bg-yellow-500 text-white rounded">Pindah</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '../services/api';
export default {
  props: { asset: { type: Object, required: true } },
  setup(props, { emit }) {
    const to_location = ref('');
    const performed_by = ref('');
    const note = ref('');

    async function doMove() {
      try {
        await api.moveAsset(props.asset.id, {
          to_location: to_location.value,
          performed_by: performed_by.value,
          note: note.value
        });
        emit('moved');
      } catch (err) {
        console.error(err);
        alert('Gagal memindahkan aset.');
      }
    }

    return { to_location, performed_by, note, doMove };
  }
};
</script>
