import { useNavigate } from "react-router-dom";

function PostSurveyPage() {
  const navigate = useNavigate();

  const finishExperiment = () => {
    localStorage.removeItem("condition");
    localStorage.removeItem("participant_id");

    navigate("/thank-you");
  };

  return (
    <div className="min-h-screen">

      <iframe
        src="https://sosci.rlp.net/nikhil/"
        title="Post Survey"
        className="w-full h-[90vh] border-0"
      />

      <div className="flex justify-center py-6">
        <button
          onClick={finishExperiment}
          className="
            bg-green-600
            hover:bg-green-700
            text-white
            px-8
            py-3
            rounded-xl
            font-semibold
            transition
          "
        >
          Submit Experiment
        </button>
      </div>

    </div>
  );
}

export default PostSurveyPage;