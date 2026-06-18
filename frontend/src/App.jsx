import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import ThankYouPage from "./pages/ThankYouPage";
import ExperimentStartPage from "./pages/ExperimentStartPage";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <BrowserRouter>
      <Routes>

        <Route path="/thank-you" element={<ThankYouPage />} />

        <Route path="/experiment" element={<ExperimentStartPage />} />

        <Route path="/" element={<HomePage darkMode={darkMode} setDarkMode={setDarkMode} />} />

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
