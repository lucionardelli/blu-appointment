import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
import es from "./locales/es.json";

const savedLanguage = localStorage.getItem("language") || "en";
document.documentElement.lang = savedLanguage;

const i18n = createI18n({
  legacy: false, // you must set `legacy: false` to use Composition API
  locale: savedLanguage, // set default locale
  fallbackLocale: "en",
  messages: {
    en,
    es,
  },
});

export default i18n;
