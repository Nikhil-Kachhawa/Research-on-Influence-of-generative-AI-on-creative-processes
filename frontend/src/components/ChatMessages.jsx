import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

function ChatMessages({
  messages,
  loading,
  darkMode,
  role,
}) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div
      className={`h-[65vh] overflow-y-auto p-6 md:p-8 ${
        darkMode
          ? "bg-[#141B34]"
          : "bg-white "
      }`}
    >
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full ">
          <div className="text-center">

            <div className="text-6xl mb-4">
              {role === "idea-generator"
                ? "💡"
                : "🔍"}
            </div>

            <h2 className="text-3xl font-bold mb-4">
              {role === "idea-generator"
                ? "Idea Generator"
                : "Critical Evaluator"}
            </h2>

            <p
              className={
                darkMode
                  ? "text-gray-400"
                  : "text-gray-600"
              }
            >
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
                    : "bg-gray-100 border border-red-300 text-gray-800"
                }`}
              >
                {message.sender === "ai" ? (
                  <ReactMarkdown
                    components={{
                      h1: ({ children }) => (
                        <h1 className="text-3xl font-bold text-red-500 mb-4 ">
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
                        <p className="mb-3 leading-8">
                          {children}
                        </p>
                      ),

                      ul: ({ children }) => (
                        <ul className="list-disc ml-6 mb-4 space-y-2">
                          {children}
                        </ul>
                      ),

                      ol: ({ children }) => (
                        <ol className="list-decimal ml-6 mb-4 space-y-2">
                          {children}
                        </ol>
                      ),

                      strong: ({ children }) => (
                        <strong className="font-semibold">
                          {children}
                        </strong>
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

          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}

export default ChatMessages;