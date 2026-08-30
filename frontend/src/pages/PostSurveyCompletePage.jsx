import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import api from "../services/api";

function PostSurveyCompletePage() {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const hasRun = useRef(false);

  // loading | continue | completed
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    if (hasRun.current) return;

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

        // -------------------------------
        // Experiment Finished
        // -------------------------------
        if (res.data.status === "completed") {
          setStatus("completed");

          setTimeout(() => {
            navigate("/thank-you");
          }, 6000);

          return;
        }

        // -------------------------------
        // Continue to Chat 2
        // -------------------------------
        setStatus("continue");

        setTimeout(() => {
          if (res.data.current_role === "idea-generator") {
            navigate("/agent1");
            return;
          }

          if (res.data.current_role === "critical-evaluator") {
            navigate("/agent2");
            return;
          }

          navigate("/");
        }, 7000);
      } catch (error) {
        console.error(error);
        navigate("/");
      }
    };

    continueExperiment();
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-6">
      <div className="max-w-2xl text-center bg-white rounded-2xl shadow-lg p-10">

        <div className="text-6xl mb-6">🧪</div>

        {/* ---------------- Loading ---------------- */}

        {status === "loading" && (
          <>
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              {t("common.loading")}
            </h1>

            <p className="text-lg text-gray-600 leading-relaxed mb-8">
              {t("survey.pleaseWait")}
            </p>
          </>
        )}

        {/* ---------------- Continue ---------------- */}

        {status === "continue" && (
          <>
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              {t("continueExperiment.title")}
            </h1>

            <p className="text-lg text-gray-600 leading-relaxed mb-8">
              {t("continueExperiment.message")}
            </p>
          </>
        )}

        {/* ---------------- Completed ---------------- */}

        {status === "completed" && (
          <>
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              {t("experimentComplete.title")}
            </h1>

            <p className="text-lg text-gray-600 leading-relaxed mb-8">
              {t("experimentComplete.message")}
            </p>
          </>
        )}

        <div className="flex justify-center items-center gap-3 mt-4">
          <div className="w-5 h-5 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>

          <span className="text-gray-600 font-medium">
            {status === "loading" && t("common.loading")}

            {status === "continue" &&
              t("continueExperiment.loading")}

            {status === "completed" &&
              t("experimentComplete.loading")}
          </span>
        </div>
      </div>
    </div>
  );
}

export default PostSurveyCompletePage;