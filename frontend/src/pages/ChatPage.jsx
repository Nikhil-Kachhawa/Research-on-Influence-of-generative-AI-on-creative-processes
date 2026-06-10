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
    <div className="app-container">

      <h1 className="title">
        {role === "idea-generator"
          ? "Idea Generator"
          : "Critical Evaluator"}
      </h1>
    <div className="input-container">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your thesis idea..."
      />

      <button onClick={sendMessage}>
        Send
      </button>

      <div className="response">
        {response}
      </div>
      </div>
    </div>
  );
}

export default ChatPage;