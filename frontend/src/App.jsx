import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";

import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import ThankYouPage from "./pages/ThankYouPage";
import ExperimentStartPage from "./pages/ExperimentStartPage";
import PostSurveyCompletePage from "./pages/PostSurveyCompletePage";
import DashboardPage from "./pages/DashBoardPage";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/thank-you" element={<ThankYouPage />} />

        <Route
          path="/post-survey-complete"
          element={<PostSurveyCompletePage />}
        />

        <Route path="/experiment" element={<ExperimentStartPage />} />

        <Route
          path="/"
          element={<HomePage darkMode={darkMode} setDarkMode={setDarkMode} />}
        />

        <Route path="/dashboard" element={<DashboardPage />} />

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
