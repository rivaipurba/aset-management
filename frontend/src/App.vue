<template>
  <div class="min-h-screen flex bg-gray-50 dark:bg-slate-900 text-slate-800 dark:text-slate-100">
    <!-- Mobile overlay & drawer -->
    <transition name="fade">
      <div v-if="mobileOpen" class="fixed inset-0 bg-black bg-opacity-30 z-30" @click="mobileOpen = false"></div>
    </transition>

    <!-- Sidebar (desktop) -->
    <div class="hidden md:block">
      <Sidebar />
    </div>

    <!-- Mobile topbar -->
    <div class="md:hidden fixed top-0 left-0 right-0 z-20 bg-white dark:bg-slate-800 border-b dark:border-slate-700">
      <div class="flex items-center justify-between px-3 py-2">
        <div class="flex items-center gap-2">
          <button @click="mobileOpen = true" class="p-2 rounded hover:bg-slate-100 dark:hover:bg-slate-700">
            <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </button>
          <div class="text-lg font-semibold">Aset TI</div>
        </div>

        <div class="flex items-center gap-2">
          <div class="text-sm text-slate-500 dark:text-slate-300 hidden sm:block">Manajemen Aset</div>
        </div>
      </div>
    </div>

    <!-- Mobile drawer -->
    <transition name="slide">
      <div v-if="mobileOpen" class="fixed inset-y-0 left-0 z-40 w-72 bg-white dark:bg-slate-800 border-r dark:border-slate-700 md:hidden">
        <Sidebar />
      </div>
    </transition>

    <!-- main content -->
    <div class="flex-1 min-h-screen">
      <!-- header area for desktop (optional small bar) -->
      <header class="hidden md:flex items-center justify-between px-6 py-3 border-b dark:border-slate-700 bg-white dark:bg-slate-800">
        <div class="text-lg font-semibold">Manajemen Aset</div>
        <div class="text-sm text-slate-500 dark:text-slate-300">Selamat datang</div>
      </header>

      <!-- content area: SINGLE router-view -->
      <main class="p-4 md:p-6">
        <router-view />
      </main>

      <!-- Toast global (only once in app) -->
      <Toast />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Sidebar from './components/Sidebar.vue';
import Toast from './components/Toast.vue';

const mobileOpen = ref(false);

function handleSidebarClose() { mobileOpen.value = false; }
onMounted(() => { window.addEventListener('sidebar:close', handleSidebarClose); });
onUnmounted(() => { window.removeEventListener('sidebar:close', handleSidebarClose); });
</script>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-enter-active { transition: transform .18s ease; transform-origin: left; }
.slide-enter-from { transform: translateX(-12%); }
.slide-leave-active { transition: transform .18s ease; }
.slide-leave-to { transform: translateX(-12%); }
</style>
