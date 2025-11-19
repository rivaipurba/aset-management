import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/main.css'; // optional - create file or remove if not using

const app = createApp(App);
app.use(router);
app.mount('#app');
