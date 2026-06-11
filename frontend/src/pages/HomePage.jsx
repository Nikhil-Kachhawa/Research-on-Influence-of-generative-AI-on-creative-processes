import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="min-h-screen bg-[#0B1020] text-white">

      <div className="border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-6 py-5 flex justify-between items-center">

          <div>
            <h1 className="text-3xl font-bold">
              Research Lab AI
            </h1>
            <p className="text-gray-400">
              University of Koblenz
            </p>
          </div>

        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-20 text-center">

        <h2 className="text-5xl font-bold mb-6">
          AI Support for Creative Tasks
        </h2>

        <p className="text-xl text-gray-300 mb-12">
          Explore different AI assistant roles for idea generation and critical evaluation.
        </p>

        <div className="grid md:grid-cols-2 gap-8">

          <Link
            to="/idea-generator"
            className="bg-[#141B34] hover:bg-[#1b2548] rounded-2xl p-8 transition"
          >
            <h3 className="text-3xl font-bold mb-4">
              💡 Idea Generator
            </h3>

            <p className="text-gray-300">
              Generate innovative and creative thesis ideas.
            </p>
          </Link>

          <Link
            to="/critical-evaluator"
            className="bg-[#141B34] hover:bg-[#1b2548] rounded-2xl p-8 transition"
          >
            <h3 className="text-3xl font-bold mb-4">
              🔍 Critical Evaluator
            </h3>

            <p className="text-gray-300">
              Critically evaluate ideas and identify strengths and weaknesses.
            </p>
          </Link>

        </div>

      </div>

    </div>
  );
}

export default HomePage;