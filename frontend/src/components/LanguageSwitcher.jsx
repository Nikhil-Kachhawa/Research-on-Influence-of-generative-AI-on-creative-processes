import { useTranslation } from "react-i18next";

function LanguageSwitcher({ darkMode }) {
  const { i18n } = useTranslation();

  const changeLanguage = (language) => {
    i18n.changeLanguage(language);
  };

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={() => changeLanguage("en")}
        className={`px-4 py-2 rounded-xl border transition ${
          i18n.language === "en"
            ? "bg-red-600 text-white border-red-600"
            : darkMode
            ? "border-gray-700 hover:border-red-500"
            : "border-red-300 hover:border-red-500"
        }`}
      >
        EN
      </button>

      <button
        onClick={() => changeLanguage("de")}
        className={`px-4 py-2 rounded-xl border transition ${
          i18n.language === "de"
            ? "bg-red-600 text-white border-red-600"
            : darkMode
            ? "border-gray-700 hover:border-red-500"
            : "border-red-300 hover:border-red-500"
        }`}
      >
        DE
      </button>
    </div>
  );
}

export default LanguageSwitcher;