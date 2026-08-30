import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { useTheme } from "../context/ThemeContext";
import LanguageSwitcher from "../components/LanguageSwitcher";
import universityLogo from "../assets/uk.svg";
import api from "../services/api";

function HomePage() {
  const navigate = useNavigate();

  const { darkMode, toggleTheme } = useTheme();

  const { t } = useTranslation();

  useEffect(() => {
    document.title = t("header.title");
  }, [t]);

  const startExperiment = async () => {
    try {
      const res = await api.post("start-experiment/");

      localStorage.setItem("participant_id", res.data.participant_id);

      localStorage.setItem("participant_number", res.data.participant_number);

      localStorage.setItem("session_id", res.data.session_id);

      if (res.data.current_role === "idea-generator") {
        navigate("/agent1");
      } else {
        navigate("/agent2");
      }
    } catch (error) {
      console.error(error);
      alert("Unable to start the experiment.");
    }
  };

  return (
    <div
      className={`min-h-screen overflow-x-hidden transition-colors duration-300 ${
        darkMode ? "dark-scrollbar" : "light-scrollbar"
      } ${darkMode ? "bg-[#0B1020] text-white" : "bg-white text-black"}`}
    >
      {/* Header */}
      <header className="border-b border-red-500/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 md:px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3 md:gap-4">
            <img
              src={universityLogo}
              alt="UK Logo"
              className="h-12 md:h-16 w-auto cursor-pointer transition duration-300 hover:scale-105"
              onClick={() => navigate("/")}
            />

            <div>
              <h1
                className={`font-bold text-lg md:text-2xl ${
                  darkMode ? "text-white" : "text-black"
                }`}
              >
                {t("header.title")}
              </h1>

              <p
                className={`text-sm ${
                  darkMode ? "text-red-500" : "text-red-600"
                }`}
              >
                {t("header.subtitle")}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <LanguageSwitcher darkMode={darkMode} />

            <button
              onClick={toggleTheme}
              className={`px-4 py-2 rounded-full border transition ${
                darkMode
                  ? "bg-[#141B34] border-gray-700 hover:border-red-500"
                  : "bg-white border-red-200 hover:border-red-500"
              }`}
            >
              {darkMode ? "🌞" : "🌙"}
            </button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pt-6 pb-12 text-center">
        <h2 className="font-bold leading-tight mb-6 text-4xl sm:text-5xl lg:text-6xl">
          {t("homepage.heroTitle1")}

          <span className="text-red-600 block md:inline">
            {" "}
            {t("homepage.heroTitle2")}{" "}
          </span>

          {t("homepage.heroTitle3")}
        </h2>

        <p
          className={`max-w-3xl mx-auto text-base md:text-lg lg:text-xl leading-relaxed ${
            darkMode ? "text-gray-300" : "text-gray-700"
          }`}
        >
          {t("homepage.heroDescription")}
        </p>
      </section>

      {/* Experiment Card */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pb-16">
        <div
          className={`rounded-3xl border p-10 text-center shadow-xl ${
            darkMode
              ? "bg-[#141B34] border-gray-800"
              : "bg-white border-red-200"
          }`}
        >
          <h3 className="text-3xl font-bold mb-6">{t("homepage.cardTitle")}</h3>

          <p className={`mb-8 ${darkMode ? "text-gray-300" : "text-gray-700"}`}>
            {t("homepage.cardDescription")}
          </p>

          <button
            onClick={startExperiment}
            className="
              bg-red-600
              hover:bg-red-700
              text-white
              px-8
              py-4
              rounded-xl
              font-semibold
              transition
            "
          >
            {t("homepage.startButton")}
          </button>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
