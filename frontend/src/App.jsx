import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<HomePage />}
        />

        <Route
          path="/idea-generator"
          element={
            <ChatPage role="idea-generator" />
          }
        />

        <Route
          path="/critical-evaluator"
          element={
            <ChatPage role="critical-evaluator" />
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;