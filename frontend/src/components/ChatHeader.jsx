import { Link } from "react-router-dom";
import universityLogo from "../assets/uk.svg";

function ChatHeader({
  role,
  darkMode,
  setDarkMode,
}) {
  return (
    <header className="border-b border-red-500/30">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">

        <div className="flex items-center gap-4">
          <img
            src={universityLogo}
            alt="UK Logo"
            className="h-12 md:h-16"
          />

          <div>
            <h1 className="font-bold text-xl">
              Generative AI Research Lab
            </h1>

            <p className="text-red-500 text-sm">
              University of Koblenz
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">

          <Link
            to="/"
            className="h-12 px-5 rounded-full border flex items-center border-red-500"
          >
            🏠 Home
          </Link>

          <div className="h-12 px-5 rounded-full border flex items-center border-red-500">
            {role === "idea-generator"
              ? "💡 Idea Generator"
              : "🔍 Critical Evaluator"}
          </div>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className="h-12 w-12 rounded-full border border-red-500"
          >
            {darkMode ? "☀️" : "🌙"}
          </button>

        </div>
      </div>
    </header>
  );
}

export default ChatHeader;