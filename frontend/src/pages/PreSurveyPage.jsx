import { useNavigate } from "react-router-dom";

function PreSurveyPage() {
  const navigate = useNavigate();

  const continueToExperiment = () => {
    const condition =
      localStorage.getItem("condition");

    if (
      condition === "idea-generator"
    ) {
      navigate("/idea-generator");
    } else {
      navigate("/critical-evaluator");
    }
  };

  return (
    <div className="min-h-screen">

      <iframe
        src="https://sosci.rlp.net/nikhil/"
        title="Pre Survey"
        className="w-full h-[90vh] border-0"
      />

      <div className="flex justify-center py-6">
        <button
          onClick={continueToExperiment}
          className="
            bg-red-600
            hover:bg-red-700
            text-white
            px-8
            py-3
            rounded-xl
            font-semibold
            transition
          "
        >
          Continue to Experiment
        </button>
      </div>

    </div>
  );
}

export default PreSurveyPage;