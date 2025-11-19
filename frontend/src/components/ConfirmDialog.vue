<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-40 p-4">
    <div class="bg-white dark:bg-slate-800 rounded-lg p-6 w-full max-w-sm shadow-xl">
      <h3 class="text-lg font-medium text-slate-900 dark:text-slate-100 mb-3">{{ title }}</h3>
      <p class="text-sm text-slate-600 dark:text-slate-300 mb-5">
        {{ message }}
      </p>
      <div class="flex justify-end gap-3">
        <button @click="$emit('cancel')" class="px-4 py-2 border rounded text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700">
          Batal
        </button>
        <button @click="$emit('confirm')" class="px-4 py-2 rounded text-sm font-medium text-white bg-red-600 hover:bg-red-500">
          Hapus
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: 'Konfirmasi' },
  message: { type: String, required: true },
});
defineEmits(['confirm', 'cancel']);
</script>
