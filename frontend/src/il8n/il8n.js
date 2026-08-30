import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./en.json";
import de from "./de.json";

const savedLanguage = localStorage.getItem("language");

const browserLanguage = navigator.language.startsWith("de")
  ? "de"
  : "en";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: en,
      },
      de: {
        translation: de,
      },
    },

    lng: savedLanguage || browserLanguage,
    fallbackLng: "en",

    interpolation: {
      escapeValue: false,
    },

    returnNull: false,
    returnEmptyString: false,
  });

i18n.on("languageChanged", (language) => {
  localStorage.setItem("language", language);
});

export default i18n;