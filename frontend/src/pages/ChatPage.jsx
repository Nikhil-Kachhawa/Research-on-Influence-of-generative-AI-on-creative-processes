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

  const [showFinishModal, setShowFinishModal] = useState(false);

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

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === "Escape") {
        setShowFinishModal(false);
      }
    };

    window.addEventListener("keydown", handleEscape);

    return () => window.removeEventListener("keydown", handleEscape);
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
        participant_id: localStorage.getItem("participant_id"),

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

  const finishExperiment = () => {
    const participantId = localStorage.getItem("participant_id");

    window.location.href = `https://sosci.rlp.net/nikhil/?q=qnr2&r=${participantId}`;
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
              onClick={() => setShowFinishModal(true)}
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

      {showFinishModal && (
        <div
          onClick={() => setShowFinishModal(false)}
          className="
            fixed
            inset-0
            z-50
            flex
            items-center
            justify-center
            bg-black/60
            backdrop-blur-sm
          "
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className={`w-full max-w-md rounded-2xl p-6 shadow-2xl ${
              darkMode
                ? "bg-[#141B34] border border-gray-700"
                : "bg-white border border-gray-200"
            }`}
          >
            <h2 className="text-2xl font-bold mb-4">Finish Experiment?</h2>

            <p
              className={`mb-6 ${darkMode ? "text-gray-300" : "text-gray-600"}`}
            >
              You will be redirected to the post-survey questionnaire. After
              proceeding, you will not be able to continue this chat session.
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowFinishModal(false)}
                className={`
                  px-4
                  py-2
                  rounded-lg
                  border
                  ${
                    darkMode
                      ? "border-gray-600 hover:bg-gray-800"
                      : "border-gray-300 hover:bg-gray-100"
                  }
                `}
              >
                Continue Chat
              </button>

              <button
                onClick={finishExperiment}
                className="
                  px-4
                  py-2
                  rounded-lg
                  bg-green-600
                  hover:bg-green-700
                  text-white
                "
              >
                Proceed to Survey
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatPage;
