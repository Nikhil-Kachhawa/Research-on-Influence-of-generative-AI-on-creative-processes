import { useState } from "react";
import api from "./services/api";

function App() {

  const [message, setMessage] = useState("");

  const testBackend = async () => {
    try {
      const response = await api.get("test/");
      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setMessage("Connection failed");
    }
  };

  return (
    <div>
      <h1>Research Lab AI</h1>

      <button onClick={testBackend}>
        Test Backend Connection
      </button>

      <h2>{message}</h2>
    </div>
  );
}

export default App;