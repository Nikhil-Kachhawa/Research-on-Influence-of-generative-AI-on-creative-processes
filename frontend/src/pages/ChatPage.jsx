import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import api from "../services/api";

function ChatPage({ role }) {
const [input, setInput] = useState("");
const [response, setResponse] = useState("");
const [loading, setLoading] = useState(false);

const sendMessage = async () => {
if (!input.trim()) return;

try {
  setLoading(true);

  const res = await api.post("chat/", {
    role: role,
    message: input,
  });

  setResponse(res.data.response);
} catch (error) {
  console.error(error);
  setResponse("Something went wrong.");
} finally {
  setLoading(false);
}


};
console.log("Response:", response);
return ( <div className="min-h-screen bg-[#0B1020] text-white">
  {/* Navbar */}
  <div className="border-b border-gray-700">
    <div className="max-w-6xl mx-auto px-6 py-5 flex justify-between items-center">

      <Link
        to="/"
        className="text-2xl font-bold hover:text-red-400 transition"
      >
        Research Lab AI
      </Link>

      <span className="text-gray-400">
        University of Koblenz
      </span>

    </div>
  </div>

  <div className="max-w-5xl mx-auto px-6 py-10">

    {/* Page Title */}
    <div className="mb-8 text-center">

      <h1 className="text-5xl font-bold mb-3">
        {role === "idea-generator"
          ? "💡 Idea Generator"
          : "🔍 Critical Evaluator"}
      </h1>

      <p className="text-gray-400">
        {role === "idea-generator"
          ? "Generate innovative and creative research ideas."
          : "Critically evaluate ideas and identify strengths and weaknesses."}
      </p>

    </div>

    {/* Response Card */}
    <div className="bg-[#141B34] rounded-2xl shadow-xl p-8 min-h-[300px] mb-6">

      {loading ? (
        <div className="flex justify-center items-center h-full">
          <p className="text-xl text-gray-300">
            Thinking...
          </p>
        </div>
      ) : response ? (
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown>
            {response}
          </ReactMarkdown>
        </div>
      ) : (
        <div className="flex justify-center items-center h-full">
          <p className="text-gray-400 text-lg">
            Ask something to get started...
          </p>
        </div>
      )}

    </div>

    {/* Input Area */}
    <div className="bg-[#141B34] rounded-2xl p-4 shadow-xl">

      <div className="flex gap-3">

        <input
          className="flex-1 rounded-xl px-4 py-4 text-black text-lg"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your thesis idea..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-[#C8102E] hover:bg-red-700 px-8 py-4 rounded-xl font-semibold transition"
        >
          Send
        </button>

      </div>

    </div>

  </div>
</div>

);
}

export default ChatPage;
