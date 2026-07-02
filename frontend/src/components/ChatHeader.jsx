import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { useTheme } from "../context/ThemeContext";

import universityLogo from "../assets/uk.svg";
import LanguageSwitcher from "./LanguageSwitcher";

function ChatHeader({ role }) {
  const { t } = useTranslation();
  const { darkMode, toggleTheme } = useTheme();
  return (
    <header className="border-b border-red-500/30">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <img src={universityLogo} alt="UK Logo" className="h-12 md:h-16" />

          <div>
            <h1 className="font-bold text-xl">{t("header.title")}</h1>

            <p className="text-red-500 text-sm">{t("header.subtitle")}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <LanguageSwitcher darkMode={darkMode} />

          <Link
            to="/"
            className="h-12 px-5 rounded-full border flex items-center border-red-500 hover:bg-red-600 hover:text-white transition"
          >
            🏠 {t("common.home")}
          </Link>

          <div className="h-12 px-5 rounded-full border flex items-center border-red-500">
            {role === "idea-generator"
              ? t("chat.ideaGenerator")
              : t("chat.criticalEvaluator")}
          </div>

          <button
            onClick={toggleTheme}
            className="h-12 w-12 rounded-full border border-red-500 hover:bg-red-600 hover:text-white transition"
            title={darkMode ? t("common.lightMode") : t("common.darkMode")}
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
        </div>
      </div>
    </header>
  );
}

export default ChatHeader;
