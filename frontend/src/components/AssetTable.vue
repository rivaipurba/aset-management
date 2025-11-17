<template>
  <table class="min-w-full text-sm text-slate-800 dark:text-slate-100">
    <thead class="bg-slate-100 dark:bg-slate-700">
      <tr>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">#</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Nama</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Seri</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Pembuat</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Pemilik</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Lokasi</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Status</th>
        <th class="px-3 py-2 border dark:border-slate-600 text-left">Aksi</th>
      </tr>
    </thead>

    <tbody>
      <tr 
        v-for="(a, index) in assets" 
        :key="a.id"
        class="hover:bg-slate-50 dark:hover:bg-slate-700/40"
      >
        <td class="px-3 py-2 border dark:border-slate-700">{{ index + 1 }}</td>
        <td class="px-3 py-2 border dark:border-slate-700 font-medium">
          {{ a.name }}
        </td>
        <td class="px-3 py-2 border dark:border-slate-700">{{ a.serial_number }}</td>
        <td class="px-3 py-2 border dark:border-slate-700">{{ a.maker }}</td>
        <td class="px-3 py-2 border dark:border-slate-700">{{ a.owner }}</td>
        <td class="px-3 py-2 border dark:border-slate-700">{{ a.location }}</td>

        <!-- Badge status -->
        <td class="px-3 py-2 border dark:border-slate-700">
          <span 
            class="px-2 py-1 text-xs rounded"
            :class="statusColor(a.status)"
          >
            {{ humanStatus(a.status) }}
          </span>
        </td>

        <!-- Action buttons -->
        <td class="px-3 py-2 border dark:border-slate-700 space-x-1">
          <button @click="$emit('view', a)"
            class="px-2 py-1 text-xs bg-gray-200 dark:bg-gray-600 rounded hover:bg-gray-300 dark:hover:bg-gray-500">
            Lihat
          </button>

          <button @click="$emit('edit', a)"
            class="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-500">
            Ubah
          </button>

          <button @click="$emit('delete', a)"
            class="px-2 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-500">
            Hapus
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
const props = defineProps({
  assets: Array,
  type: String
});

const humanStatus = (s) => {
  switch (s) {
    case "available": return "Tersedia";
    case "in_use": return "Sedang dipakai";
    case "maintenance": return "Perawatan";
    case "retired": return "Retired";
    default: return s;
  }
};

const statusColor = (s) => {
  switch (s) {
    case "available": return "bg-green-100 text-green-700 dark:bg-green-700/30 dark:text-green-300";
    case "in_use": return "bg-blue-100 text-blue-700 dark:bg-blue-700/30 dark:text-blue-300";
    case "maintenance": return "bg-yellow-100 text-yellow-700 dark:bg-yellow-700/30 dark:text-yellow-300";
    case "retired": return "bg-gray-200 text-gray-700 dark:bg-gray-700/30 dark:text-gray-300";
    default: return "bg-slate-200 text-slate-700 dark:bg-slate-700/40 dark:text-slate-300";
  }
};
</script>
