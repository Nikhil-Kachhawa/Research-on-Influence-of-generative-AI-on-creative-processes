import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";

function App() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={
            <HomePage
              darkMode={darkMode}
              setDarkMode={setDarkMode}
            />
          }
        />

        <Route
          path="/idea-generator"
          element={
            <ChatPage
              role="idea-generator"
              darkMode={darkMode}
              setDarkMode={setDarkMode}
            />
          }
        />

        <Route
          path="/critical-evaluator"
          element={
            <ChatPage
              role="critical-evaluator"
              darkMode={darkMode}
              setDarkMode={setDarkMode}
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;