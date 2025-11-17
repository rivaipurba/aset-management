<template>
  <div>
    <!-- Table for medium+ screens -->
    <div class="hidden sm:block overflow-x-auto">
      <table class="min-w-full border-collapse">
        <thead>
          <tr class="bg-gray-100 text-left">
            <th class="px-3 py-2 border text-sm">#</th>

            <!-- clickable headers: emit sort -->
            <th @click="clickSort('name')" class="px-3 py-2 border text-sm cursor-pointer select-none">
              Nama <span class="text-xs">{{ sortIndicator('name') }}</span>
            </th>

            <th @click="clickSort('serial_number')" class="px-3 py-2 border text-sm cursor-pointer select-none">
              Seri <span class="text-xs">{{ sortIndicator('serial_number') }}</span>
            </th>

            <th @click="clickSort('maker')" class="px-3 py-2 border text-sm hidden md:table-cell cursor-pointer select-none">
              Pembuat <span class="text-xs">{{ sortIndicator('maker') }}</span>
            </th>

            <th @click="clickSort('owner')" class="px-3 py-2 border text-sm hidden md:table-cell cursor-pointer select-none">
              Pemilik <span class="text-xs">{{ sortIndicator('owner') }}</span>
            </th>

            <th @click="clickSort('location')" class="px-3 py-2 border text-sm hidden md:table-cell cursor-pointer select-none">
              Lokasi <span class="text-xs">{{ sortIndicator('location') }}</span>
            </th>

            <th v-if="isComputer" class="px-3 py-2 border text-sm hidden lg:table-cell">RAM</th>
            <th v-if="isComputer" class="px-3 py-2 border text-sm hidden lg:table-cell">Penyimpanan</th>
            <th v-if="isPrinter" class="px-3 py-2 border text-sm hidden lg:table-cell">Berwarna</th>
            <th v-if="isMonitor" class="px-3 py-2 border text-sm hidden lg:table-cell">Ukuran</th>

            <th @click="clickSort('status')" class="px-3 py-2 border text-sm cursor-pointer select-none">Status <span class="text-xs">{{ sortIndicator('status') }}</span></th>
            <th @click="clickSort('condition')" class="px-3 py-2 border text-sm cursor-pointer select-none">Kondisi <span class="text-xs">{{ sortIndicator('condition') }}</span></th>
            <th class="px-3 py-2 border text-sm">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(a, idx) in assets" :key="a.id" class="odd:bg-white even:bg-gray-50 align-top">
            <td class="px-3 py-2 border text-sm">{{ idx + 1 }}</td>
            <td class="px-3 py-2 border text-sm">{{ a.name }}</td>
            <td class="px-3 py-2 border text-sm">{{ a.serial_number }}</td>
            <td class="px-3 py-2 border text-sm hidden md:table-cell">{{ a.maker }}</td>
            <td class="px-3 py-2 border text-sm hidden md:table-cell">{{ a.owner }}</td>
            <td class="px-3 py-2 border text-sm hidden md:table-cell">{{ a.location }}</td>

            <td v-if="isComputer" class="px-3 py-2 border text-sm hidden lg:table-cell">{{ a.computer_spec?.ram || '-' }}</td>
            <td v-if="isComputer" class="px-3 py-2 border text-sm hidden lg:table-cell">{{ a.computer_spec?.storage || '-' }}</td>
            <td v-if="isPrinter" class="px-3 py-2 border text-sm hidden lg:table-cell">{{ a.printer_spec?.is_color ? 'Ya' : 'Tidak' }}</td>
            <td v-if="isMonitor" class="px-3 py-2 border text-sm hidden lg:table-cell">{{ a.monitor_spec?.size_inch || '-' }}</td>

            <td class="px-3 py-2 border text-sm">{{ humanStatus(a.status) }}</td>
            <td class="px-3 py-2 border text-sm">{{ humanCondition(a.condition) }}</td>
            <td class="px-3 py-2 border text-sm">
              <div class="flex flex-wrap gap-2">
                <button @click="$emit('view', a)" class="px-2 py-1 bg-gray-600 text-white rounded-sm text-xs">Lihat</button>
                <button @click="$emit('edit', a)" class="px-2 py-1 bg-blue-600 text-white rounded-sm text-xs">Ubah</button>
                <button @click="$emit('delete', a)" class="px-2 py-1 bg-red-600 text-white rounded-sm text-xs">Hapus</button>
              </div>
            </td>
          </tr>
          <tr v-if="assets.length === 0">
            <td colspan="14" class="px-3 py-4 text-center text-gray-500">Belum ada aset</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Card list for small screens -->
    <div class="sm:hidden space-y-3">
      <div v-for="a in assets" :key="a.id" class="bg-white border rounded p-3 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <div class="font-medium">{{ a.name }}</div>
            <div class="text-xs text-gray-500">ID: {{ a.id }} • Seri: {{ a.serial_number || '-' }}</div>
          </div>
          <div class="flex gap-2">
            <button @click="$emit('view', a)" class="px-2 py-1 bg-gray-600 text-white rounded-sm text-xs">Lihat</button>
            <button @click="$emit('edit', a)" class="px-2 py-1 bg-blue-600 text-white rounded-sm text-xs">Ubah</button>
          </div>
        </div>

        <div class="mt-2 text-sm text-gray-700 space-y-1">
          <div><span class="text-gray-500 text-xs">Pembuat: </span>{{ a.maker || '-' }}</div>
          <div><span class="text-gray-500 text-xs">Pemilik: </span>{{ a.owner || '-' }}</div>
          <div><span class="text-gray-500 text-xs">Lokasi: </span>{{ a.location || '-' }}</div>
          <div><span class="text-gray-500 text-xs">Status: </span>{{ humanStatus(a.status) }}</div>
          <div><span class="text-gray-500 text-xs">Kondisi: </span>{{ humanCondition(a.condition) }}</div>
          <div v-if="isComputer"><span class="text-gray-500 text-xs">RAM: </span>{{ a.computer_spec?.ram || '-' }}</div>
        </div>
      </div>
      <div v-if="assets.length === 0" class="text-center text-gray-500">Belum ada aset</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    assets: { type: Array, required: true },
    type: { type: String, required: true },
    sortField: { type: String, default: null },
    sortDir: { type: String, default: 'asc' } // 'asc' or 'desc'
  },
  computed: {
    isComputer() { return ['laptop','pc'].includes(this.type); },
    isPrinter() { return this.type === 'printer'; },
    isMonitor() { return this.type === 'monitor'; }
  },
  methods: {
    humanStatus(v) {
      if (!v) return '-';
      const map = {
        available: 'Tersedia',
        in_use: 'Sedang dipakai',
        maintenance: 'Perawatan',
        retired: 'Pensiun'
      };
      return map[v] || v;
    },
    humanCondition(v) {
      if (!v) return '-';
      const cmap = {
        good: 'Baik',
        fair: 'Cukup',
        bad: 'Buruk'
      };
      return cmap[v] || v;
    },
    clickSort(field) {
      this.$emit('sort', field);
    },
    sortIndicator(field) {
      if (this.sortField !== field) return '';
      return this.sortDir === 'asc' ? '▲' : '▼';
    }
  }
};
</script>
