<template>
  <div class="min-h-[60vh] p-6 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 shadow">
    <h1 class="text-2xl font-semibold mb-4">Dashboard Aset TI</h1>

    <p class="text-sm text-slate-600 dark:text-slate-300 mb-6">
      Ikhtisar singkat aset Anda. (Data contoh — implementasikan data real dari API)
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="p-4 bg-white dark:bg-slate-700 border rounded shadow-sm">
        <div class="text-xs text-slate-500 dark:text-slate-300">Total Aset</div>
        <div class="text-2xl font-bold text-slate-800 dark:text-slate-50">123</div>
      </div>

      <div class="p-4 bg-white dark:bg-slate-700 border rounded shadow-sm">
        <div class="text-xs text-slate-500 dark:text-slate-300">Tersedia</div>
        <div class="text-2xl font-bold text-green-600 dark:text-green-300">23</div>
      </div>

      <div class="p-4 bg-white dark:bg-slate-700 border rounded shadow-sm">
        <div class="text-xs text-slate-500 dark:text-slate-300">Sedang dipakai</div>
        <div class="text-2xl font-bold text-blue-600 dark:text-blue-300">87</div>
      </div>

      <div class="p-4 bg-white dark:bg-slate-700 border rounded shadow-sm">
        <div class="text-xs text-slate-500 dark:text-slate-300">Dalam Perawatan</div>
        <div class="text-2xl font-bold text-yellow-600 dark:text-yellow-300">13</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// nanti sambungkan ke API dan ganti angka statis di atas
</script>

<style scoped>
/* untuk memastikan tidak ada opacity yang menurunkan teks */
:root, .dashboard-root {
  color: inherit;
  opacity: 1;
}
</style>
