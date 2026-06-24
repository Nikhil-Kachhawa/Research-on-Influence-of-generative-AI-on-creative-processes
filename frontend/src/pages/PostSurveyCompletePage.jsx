import { useEffect } from "react";
import api from "../services/api";
import ThankYouPage from "./ThankYouPage";

function PostSurveyCompletePage() {
  useEffect(() => {
    const participantId = new URLSearchParams(window.location.search).get("r");

    api.post("complete-survey/", {
      participant_id: participantId,
      survey_type: "post",
    });
  }, []);

  return <ThankYouPage />;
}

export default PostSurveyCompletePage;
