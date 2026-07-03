import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import api from "../services/api";

function PostSurveyCompletePage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const hasRun = useRef(false);
  useEffect(() => {
    if (hasRun.current) {
      return;
    }

    hasRun.current = true;

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

        if (res.data.session_id) {
          localStorage.setItem("session_id", res.data.session_id);
        }

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
          {t("continueExperiment.title")}
          </h1>

        <p className="text-gray-600">
          {t("continueExperiment.message")}
        </p>
      </div>
    </div>
  );
}

export default PostSurveyCompletePage;
