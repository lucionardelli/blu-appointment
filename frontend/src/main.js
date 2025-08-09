import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import createI18n from "./i18n";
import "./assets/main.css";
import "./services/api";

const i18n = createI18n();

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(i18n);

app.mount("#app");
