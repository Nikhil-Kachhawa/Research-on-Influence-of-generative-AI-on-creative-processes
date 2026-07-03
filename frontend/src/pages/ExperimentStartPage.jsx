import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useTranslation } from "react-i18next";

function ExperimentStartPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  useEffect(() => {
    const startExperiment = async () => {
      try {
        const participantId = localStorage.getItem("participant_id");

        await api.post("complete-survey/", {
          participant_id: participantId,

          survey_type: "pre",
        });

        const condition = localStorage.getItem("condition");

        if (condition === "idea-generator") {
          navigate("/idea-generator");
        } else {
          navigate("/critical-evaluator");
        }
      } catch (error) {
        console.error(error);

        navigate("/");
      }
    };

    startExperiment();
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      { t("common.loadingExperiment") }
    </div>
  );
}

export default ExperimentStartPage;
