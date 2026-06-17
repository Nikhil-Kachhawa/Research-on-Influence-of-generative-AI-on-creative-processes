import { getSessionId } from "../utils/session";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api, { getChatHistory } from "../services/api";

import ChatHeader from "../components/ChatHeader";
import ChatMessages from "../components/ChatMessages";
import ChatInput from "../components/ChatInput";

function ChatPage({ role, darkMode, setDarkMode }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    document.title =
      role === "idea-generator" ? "Idea Generator" : "Critical Evaluator";
  }, [role]);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getChatHistory(getSessionId(role));

        const history = [];

        data.messages.forEach((msg) => {
          history.push({
            sender: "user",
            content: msg.user_message,
          });

          history.push({
            sender: "ai",
            content: msg.ai_response,
          });
        });

        setMessages(history);
      } catch (error) {
        console.error("Failed to load history", error);
      }
    };

    loadHistory();
  }, []);

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
        session_id: getSessionId(role),
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
      className={`min-h-screen ${
        darkMode ? "bg-[#0B1020] text-white" : "bg-white text-black"
      }`}
    >
      <ChatHeader role={role} darkMode={darkMode} setDarkMode={setDarkMode} />

      <main className="max-w-6xl mx-auto px-4 py-6">
        <div
          className={`rounded-3xl border shadow-xl overflow-hidden ${
            darkMode
              ? "bg-[#141B34] border-gray-800"
              : "bg-white border-red-200"
          }`}
        >
          <ChatMessages
            messages={messages}
            loading={loading}
            darkMode={darkMode}
            role={role}
          />

          <ChatInput
            input={input}
            setInput={setInput}
            sendMessage={sendMessage}
            loading={loading}
            darkMode={darkMode}
          />

          <div className="flex justify-center py-4">
            <button
              onClick={() => navigate("/survey/post")}
              className="
                  bg-green-600
                  hover:bg-green-700
                  text-white
                  px-6
                  py-2
                  rounded-lg
                  font-semibold
    "
            >
              Finish Experiment
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ChatPage;
