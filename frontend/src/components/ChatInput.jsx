function ChatInput({
  input,
  setInput,
  sendMessage,
  loading,
  darkMode,
}) {
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
          value={input}
          onChange={(e) =>
            setInput(e.target.value)
          }
          onKeyDown={(e) =>
            e.key === "Enter" && sendMessage()
          }
          placeholder="Enter your thesis idea..."
          className={`flex-1 rounded-2xl px-4 py-4 border ${
            darkMode
              ? "bg-[#0B1020] border-gray-700"
              : "bg-gray-50 border-gray-300"
          }`}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-8 py-4 rounded-2xl bg-red-600 text-white"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatInput;