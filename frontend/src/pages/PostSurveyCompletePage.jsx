import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function PostSurveyCompletePage() {
  const navigate = useNavigate();

  useEffect(() => {
    const continueExperiment = async () => {
      try {
        const participantId = localStorage.getItem("participant_id");

        if (!participantId) {
          navigate("/");
          return;
        }

        const res = await api.post("continue-experiment/", {
          participant_id: participantId,
        });

        if (res.data.status === "completed") {
          navigate("/thank-you");
          return;
        }

        if (res.data.current_role === "idea-generator") {
          navigate("/idea-generator");
          return;
        }

        if (res.data.current_role === "critical-evaluator") {
          navigate("/critical-evaluator");
          return;
        }

        navigate("/");
      } catch (error) {
        console.error(error);
        navigate("/");
      }
    };

    continueExperiment();
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">

        <h1 className="text-3xl font-bold mb-4">
          Preparing the next step...
        </h1>

        <p className="text-gray-600">
          Please wait while your experiment is continued.
        </p>

      </div>
    </div>
  );
}

export default PostSurveyCompletePage;