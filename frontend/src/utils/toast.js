// src/utils/toast.js
import { reactive } from 'vue';

export const toastState = reactive({
  list: []
});

/**
 * addToast(message, type='info', ttl=3000)
 */
export function addToast(message, type = 'info', ttl = 3000) {
  const id = Date.now() + Math.floor(Math.random() * 1000);
  toastState.list.push({ id, message, type });

  // remove after ttl
  setTimeout(() => {
    const idx = toastState.list.findIndex(t => t.id === id);
    if (idx !== -1) toastState.list.splice(idx, 1);
  }, ttl);
}

export function toastSuccess(msg, ttl = 3000) {
  addToast(msg, 'success', ttl);
}

export function toastError(msg, ttl = 5000) {
  addToast(msg, 'error', ttl);
}

export function toastInfo(msg, ttl = 3000) {
  addToast(msg, 'info', ttl);
}
