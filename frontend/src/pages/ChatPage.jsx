import { useState } from "react";
import api from "../services/api";

function ChatPage({ role }) {

  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {

    try {

      const res = await api.post("chat/", {
        role: role,
        message: input
      });

      setResponse(res.data.response);

    } catch (error) {
      console.error(error);
    }

  };

  return (
    <div>

      <h1>
        {role === "idea-generator"
          ? "Idea Generator"
          : "Critical Evaluator"}
      </h1>

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your thesis idea..."
      />

      <button onClick={sendMessage}>
        Send
      </button>

      <h3>{response}</h3>

    </div>
  );
}

export default ChatPage;