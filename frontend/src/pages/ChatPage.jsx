import { getSessionId } from "../utils/session";
import { useState, useEffect } from "react";
import api from "../services/api";

import ChatHeader from "../components/ChatHeader";
import ChatMessages from "../components/ChatMessages";
import ChatInput from "../components/ChatInput";

function ChatPage({ role, darkMode, setDarkMode }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title =
      role === "idea-generator"
        ? "Idea Generator"
        : "Critical Evaluator";
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
      className={`min-h-screen ${
        darkMode
          ? "bg-[#0B1020] text-white"
          : "bg-white text-black"
      }`}
    >
      <ChatHeader
        role={role}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />

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
        </div>
      </main>
    </div>
  );
}

export default ChatPage;