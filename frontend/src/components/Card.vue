<template>
  <div class="relative p-5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 group overflow-hidden">
    <!-- Decorative background blob -->
    <div class="absolute -right-6 -top-6 w-24 h-24 bg-slate-50 dark:bg-slate-700/50 rounded-full transition-transform group-hover:scale-150 duration-500"></div>
    
    <div class="relative z-10 flex items-start justify-between">
      <div>
        <div v-if="title || $slots.header" class="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">
          <slot name="header">{{ title }}</slot>
        </div>
        <div class="text-3xl font-bold tracking-tight" :class="valueColor">
          <slot>{{ value }}</slot>
        </div>
      </div>
      
      <div v-if="icon || $slots.icon" class="p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50 text-slate-600 dark:text-slate-300 group-hover:bg-indigo-50 dark:group-hover:bg-indigo-900/30 group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors duration-300">
        <slot name="icon">
          <span v-html="icon" class="flex items-center justify-center w-6 h-6"></span>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  value: {
    type: [String, Number],
    default: ''
  },
  valueColor: {
    type: String,
    default: 'text-slate-800 dark:text-slate-100'
  },
  icon: {
    type: String,
    default: ''
  }
});
</script>
