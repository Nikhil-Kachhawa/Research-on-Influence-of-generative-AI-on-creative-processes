import { getSessionId } from "../utils/session";
import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Link } from "react-router-dom";
import api from "../services/api";
import universityLogo from "../assets/uk.svg";

function ChatPage({ role, darkMode, setDarkMode }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title =
      role === "idea-generator" ? "Idea Generator" : "Critical Evaluator";
  }, [role]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        content: userMessage,
      },
    ]);

    setInput("");

    try {
      setLoading(true);

      const res = await api.post("chat/", {
        session_id: getSessionId(),
        role,
        message: userMessage,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          content: res.data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          content: "Something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen overflow-x-hidden transition-colors duration-300 ${
        darkMode ? "dark-scrollbar" : "light-scrollbar"
      } ${darkMode ? "bg-[#0B1020] text-white" : "bg-white text-black"}`}
    >
      {/* Header */}
      <header className="border-b border-red-500/30">
        <div className="max-w-7xl mx-auto px-4 md:px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <img
              src={universityLogo}
              alt="UK Logo"
              className="h-12 md:h-16 w-auto"
            />

            <div>
              <h1 className="font-bold text-lg md:text-2xl">
                Generative AI Research Lab
              </h1>

              <p className="text-red-500 text-sm">University of Koblenz</p>
            </div>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <Link
              to="/"
              className={`h-12 px-6 rounded-full border flex items-center justify-center gap-2 transition ${
                darkMode
                  ? "bg-[#141B34] border-gray-700 hover:border-red-500 text-red-400"
                  : "bg-white border-red-200 hover:border-red-500 text-red-600"
              }`}
            >
              🏠 Home
            </Link>

            <div
              className={`h-12 px-6 rounded-full border flex items-center justify-center gap-2 ${
                darkMode
                  ? "bg-[#141B34] text-red-400 border-red-500/20"
                  : "bg-red-50 text-red-600 border-red-200"
              }`}
            >
              {role === "idea-generator"
                ? "💡 Idea Generator"
                : "🔍 Critical Evaluator"}
            </div>

            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`h-12 w-12 rounded-full border flex items-center justify-center transition ${
                darkMode
                  ? "bg-[#141B34] border-gray-700 hover:border-red-500"
                  : "bg-white border-red-200 hover:border-red-500"
              }`}
            >
              {darkMode ? "☀️" : "🌙"}
            </button>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-6xl mx-auto px-4 md:px-6 py-6">
        <div
          className={`rounded-3xl border shadow-xl overflow-hidden ${
            darkMode
              ? "bg-[#141B34] border-gray-800"
              : "bg-white border-red-200"
          }`}
        >
          {/* Response */}
          <div
            className={`h-[65vh] overflow-y-auto p-6 md:p-8 ${
              darkMode ? "bg-[#141B34]" : "bg-white"
            }`}
          >
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="text-6xl mb-4">
                    {role === "idea-generator" ? "💡" : "🔍"}
                  </div>

                  <h2 className="text-3xl font-bold mb-4">
                    {role === "idea-generator"
                      ? "Idea Generator"
                      : "Critical Evaluator"}
                  </h2>

                  <p className={darkMode ? "text-gray-400" : "text-gray-600"}>
                    {role === "idea-generator"
                      ? "Generate innovative research topics."
                      : "Analyze and improve research ideas."}
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${
                      message.sender === "user"
                        ? "justify-end"
                        : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-[85%] rounded-3xl px-5 py-4 ${
                        message.sender === "user"
                          ? "bg-red-500 text-white"
                          : darkMode
                            ? "bg-[#0B1020] border border-gray-700 text-gray-200"
                            : "bg-gray-100 border border-gray-300 text-gray-800"
                      }`}
                    >
                      {message.sender === "ai" ? (
                        <ReactMarkdown
                          components={{
                            h1: ({ children }) => (
                              <h1 className="text-3xl font-bold text-red-500 mb-4">
                                {children}
                              </h1>
                            ),

                            h2: ({ children }) => (
                              <h2 className="text-2xl font-bold text-red-500 mt-6 mb-3">
                                {children}
                              </h2>
                            ),

                            h3: ({ children }) => (
                              <h3 className="text-xl font-semibold text-red-500 mt-4 mb-2">
                                {children}
                              </h3>
                            ),

                            p: ({ children }) => (
                              <p className="mb-3 leading-8">{children}</p>
                            ),

                            ul: ({ children }) => (
                              <ul className="list-disc ml-6 space-y-2 mb-4">
                                {children}
                              </ul>
                            ),

                            ol: ({ children }) => (
                              <ol className="list-decimal ml-6 space-y-2 mb-4">
                                {children}
                              </ol>
                            ),
                          }}
                        >
                          {message.content}
                        </ReactMarkdown>
                      ) : (
                        <p>{message.content}</p>
                      )}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex justify-start">
                    <div
                      className={`rounded-3xl px-5 py-4 ${
                        darkMode
                          ? "bg-[#0B1020] border border-gray-700"
                          : "bg-gray-100 border border-gray-300"
                      }`}
                    >
                      🤖 Thinking...
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Input */}
          <div
            className={`border-t p-4 ${
              darkMode ? "border-gray-800" : "border-red-100"
            }`}
          >
            <div className="flex flex-col md:flex-row gap-3">
              <input
                type="text"
                value={input}
                placeholder="Enter your thesis idea..."
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    sendMessage();
                  }
                }}
                className={`flex-1 rounded-2xl px-4 py-4 border outline-none ${
                  darkMode
                    ? "bg-[#0B1020] border-gray-700 text-white"
                    : "bg-gray-50 border-gray-300 text-black"
                }`}
              />

              <button
                onClick={sendMessage}
                disabled={loading}
                className="px-8 py-4 rounded-2xl bg-red-600 hover:bg-red-700 text-white font-semibold transition"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ChatPage;
