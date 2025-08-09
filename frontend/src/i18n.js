import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
import es from "./locales/es.json";

export default function () {
  return createI18n({
    locale: "en", // set default locale
    fallbackLocale: "en",
    messages: {
      en,
      es,
    },
  });
}
