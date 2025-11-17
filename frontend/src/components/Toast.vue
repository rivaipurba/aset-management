<!-- src/components/Toast.vue -->
<template>
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-2 items-end pointer-events-none">
    <transition-group name="toast" tag="div">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="pointer-events-auto max-w-sm w-full px-4 py-2 rounded shadow text-white flex items-center gap-3"
        :class="{
          'bg-green-600': t.type === 'success',
          'bg-red-600': t.type === 'error',
          'bg-blue-600': t.type === 'info'
        }"
      >
        <div class="flex-1 text-sm">{{ t.message }}</div>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { toastState } from '../utils/toast';

export default {
  name: 'Toast',
  setup() {
    return { toasts: toastState.list };
  }
};
</script>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all .2s ease; }
.toast-enter-from { opacity: 0; transform: translateY(-8px) scale(.98); }
.toast-leave-to { opacity: 0; transform: translateY(-8px) scale(.98); }
</style>
