import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
import es from "./locales/es.json";

export default function (locale) {
  return createI18n({
    locale: locale || "en",
    fallbackLocale: "en",
    messages: {
      en,
      es,
    },
  });
}
