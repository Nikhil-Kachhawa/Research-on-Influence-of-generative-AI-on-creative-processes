import { useTranslation } from "react-i18next";

function ChatInput({
  input,
  setInput,
  sendMessage,
  loading,
  darkMode,
}) {
  const { t } = useTranslation();

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) {
      sendMessage();
    }
  };

  return (
    <div
      className={`border-t p-4 ${
        darkMode
          ? "border-gray-800"
          : "border-red-100"
      }`}
    >
      <div className="flex gap-3">

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t("chat.placeholder")}
          disabled={loading}
          className={`flex-1 rounded-2xl px-4 py-4 border outline-none transition ${
            darkMode
              ? "bg-[#0B1020] border-gray-700 focus:border-red-500"
              : "bg-gray-50 border-gray-300 focus:border-red-500"
          } ${
            loading
              ? "opacity-70 cursor-not-allowed"
              : ""
          }`}
        />

        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          className={`px-8 py-4 rounded-2xl text-white font-medium transition ${
            loading || !input.trim()
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-red-600 hover:bg-red-700"
          }`}
        >
          {t("common.send")}
        </button>

      </div>
    </div>
  );
}

export default ChatInput;