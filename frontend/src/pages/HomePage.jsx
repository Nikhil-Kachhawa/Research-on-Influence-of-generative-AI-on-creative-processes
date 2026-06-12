import { Link } from "react-router-dom";
import { useEffect } from "react";
import universityLogo from "../assets/uk.svg";

function HomePage({ darkMode, setDarkMode }) {
  useEffect(() => {
    document.title = "Generative AI Research Lab";
  }, []);

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
              onClick={() => setDarkMode(!darkMode)}
            />

            <div>
              <h1
                className={`font-bold text-lg md:text-2xl ${
                  darkMode ? "text-white" : "text-black"
                }`}
              >
                Generative AI Research Lab
              </h1>

              <p
                className={`text-sm ${
                  darkMode ? "text-red-500" : "text-red-600"
                }`}
              >
                University of Koblenz
              </p>
            </div>
          </div>

          {/* <span
            className={`px-4 py-2 rounded-full text-sm font-medium ${
              darkMode
                ? "bg-[#141B34] text-red-400 border border-red-500/20"
                : "bg-red-50 text-red-600 border border-red-200"
            }`}
          >
            Research Internship Project
          </span> */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`px-4 py-2 rounded-full border transition ${
              darkMode
                ? "bg-[#141B34] border-gray-700 hover:border-red-500"
                : "bg-white border-red-200 hover:border-red-500"
            }`}
          >
            {darkMode ? "☀️" : "🌙"}
          </button>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pt-6 md: pb-12 text-center">
        <h2 className="font-bold leading-tight mb-6 text-4xl sm:text-5xl lg:text-6xl">
          AI Support for
          <span className="text-red-600 block md:inline"> Creative Tasks </span>
          in Thesis Topic Development
        </h2>

        <p
          className={`max-w-3xl mx-auto text-base md:text-lg lg:text-xl leading-relaxed ${
            darkMode ? "text-gray-300" : "text-gray-700"
          }`}
        >
          Explore how different AI roles influence creativity, brainstorming,
          and critical thinking during thesis topic generation and evaluation.
        </p>
      </section>

      {/* Cards */}
      <section className="max-w-6xl mx-auto px-4 md:px-6 pb-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Idea Generator */}
          <Link
            to="/idea-generator"
            className={`group rounded-3xl p-6 md:p-8 lg:p-10 border transition-all duration-300 shadow-xl hover:-translate-y-2 hover:border-red-500 ${
              darkMode
                ? "bg-[#141B34] border-gray-800"
                : "bg-white border-red-200"
            }`}
          >
            <div className="text-5xl md:text-6xl mb-6">💡</div>

            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Idea Generator
            </h3>

            <p
              className={`leading-relaxed mb-8 ${
                darkMode ? "text-gray-300" : "text-gray-700"
              }`}
            >
              Generate innovative and creative thesis topics across different
              domains using AI-assisted brainstorming and ideation support.
            </p>

            <span className="font-semibold text-red-500 group-hover:text-red-400">
              Start Exploring →
            </span>
          </Link>

          {/* Critical Evaluator */}
          <Link
            to="/critical-evaluator"
            className={`group rounded-3xl p-6 md:p-8 lg:p-10 border transition-all duration-300 shadow-xl hover:-translate-y-2 hover:border-red-500 ${
              darkMode
                ? "bg-[#141B34] border-gray-800"
                : "bg-white border-red-200"
            }`}
          >
            <div className="text-5xl md:text-6xl mb-6">🔍</div>

            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Critical Evaluator
            </h3>

            <p
              className={`leading-relaxed mb-8 ${
                darkMode ? "text-gray-300" : "text-gray-700"
              }`}
            >
              Analyze research ideas, identify weaknesses, assess feasibility,
              and improve overall quality through structured critique.
            </p>

            <span className="font-semibold text-red-500 group-hover:text-red-400">
              Start Evaluating →
            </span>
          </Link>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
