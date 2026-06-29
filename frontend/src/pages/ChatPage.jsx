import { getSessionId } from "../utils/session";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api, { getChatHistory } from "../services/api";

import ChatHeader from "../components/ChatHeader";
import ChatMessages from "../components/ChatMessages";
import ChatInput from "../components/ChatInput";
import webgazerModule from "webgazer";
const webgazer = webgazerModule.default || webgazerModule;

function ChatPage({ role, darkMode, setDarkMode }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const isFirstMessage = useRef(true);
  const startTime = useRef(new Date());
  const endTime = useRef(new Date());
  const gazeTimeCounter = useRef(0);
  const gazeStartTime = useRef(null);
  const gazeEndTime = useRef(null);
  const responseID = useRef(null);
  const videoRef = useRef(null);
  const [error, setError] = useState(null);
  const lastHiddenTime = useRef(null);
  const totalAwayTime = useRef(0);
  const [showFinishModal, setShowFinishModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === "hidden") {
        if(webgazer){webgazer.pause()}
        // user left tab
        lastHiddenTime.current = new Date();
        gazeStartTime.current = null;
      }

      if (document.visibilityState === "visible") {
        // user came back
        if (lastHiddenTime.current) {
          const diff = (new Date().getTime() - lastHiddenTime.current.getTime()) / 1000; // seconds
          totalAwayTime.current += diff;
          lastHiddenTime.current = null;
        }
        webgazer.resume();
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, []);

  useEffect(() => {
    async function initCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        setError(err.message);
      }
    }

    initCamera();
  }, []);

  useEffect(() => {
    document.title =
      role === "idea-generator" ? "Idea Generator" : "Critical Evaluator";
  }, [role]);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getChatHistory(getSessionId(role));
        if(data.messages.length > 0){
          isFirstMessage.current = false;
          init(document.getElementById("chatBox"))
        }
        const history = [];

        data.messages.forEach((msg) => {
          history.push({
            sender: "user",
            content: msg.user_message,
          });

          history.push({
            sender: "ai",
            content: msg.ai_response,
          });
        });
        data.messages.length > 0 ? responseID.current = data.messages[data.messages.length - 1].id : 0;
        setMessages(history);
      } catch (error) {
        console.error("Failed to load history", error);
      }
    };

    loadHistory();
  }, []);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === "Escape") {
        setShowFinishModal(false);
      }
    };

    window.addEventListener("keydown", handleEscape);

    return () => window.removeEventListener("keydown", handleEscape);
  }, []);

  let updateGazeTimer = ()=>{
    gazeEndTime.current = new Date();
    gazeTimeCounter.current += (gazeEndTime.current.getTime() - gazeStartTime.current.getTime())/1000;
    gazeStartTime.current = null;
  }

  const init = async (rect) => {
    try {
      
      webgazer
        .setGazeListener((data, elapsedTime) => {
          if(document.visibilityState !== "visible"){
            console.log("not counting anythin");
            return;
          }
          if (!data && gazeStartTime.current) { 
            updateGazeTimer();
            return;
          }
          else{
            const el = document.elementFromPoint(data.x, data.y);
            const isLookingAtTarget = rect.contains(el);
            if(isLookingAtTarget && gazeStartTime.current == null){
              gazeStartTime.current = new Date();
            }else  if (!isLookingAtTarget && gazeStartTime.current){
              updateGazeTimer();
            }
          }
        })
        .showVideoPreview(false)
        .showPredictionPoints(false);

      await webgazer.begin();
    } catch (err) {
      console.error("WebGazer init failed:", err);
    }
  }
  
  let handleUserAttentionForLastResponse = async () => {
    if(isFirstMessage.current){
      isFirstMessage.current = false;
    }
    startTime.current = new Date();
    gazeStartTime.current = new Date();

  }

  let endWebGazer = async () =>{
    if(!isFirstMessage.current && startTime.current){
      endTime.current = new Date();
      let diff = (endTime.current.getTime() - startTime.current.getTime())/1000;
      if(gazeStartTime.current){ updateGazeTimer(); }
      const res = await api.post("attentionPrediction/", {
        actual_engagement: (diff - totalAwayTime.current),
        predicted_engagement: gazeTimeCounter.current,
        response_id: responseID.current
      });
    }
    gazeEndTime.current = null;
    gazeStartTime.current = null;
    gazeTimeCounter.current= 0;
    responseID.current = null;
    totalAwayTime.current = 0;
    try{
      webgazer ? webgazer.end() : 0;
    } catch{}
  }

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    await endWebGazer();
    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        content: userMessage,
      },
    ]);

    setInput("");

    try {
      setLoading(true);
      const res = await api.post("chat/", {
        participant_id: localStorage.getItem("participant_id"),

        session_id: getSessionId(role),

        role,

        message: userMessage,
      });

      responseID.current = res.data.response_id;
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          content: res.data.response,
        },
      ]);

      const rect = document.getElementById("chatBox");
      init(rect);
      handleUserAttentionForLastResponse();
      

    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          content: "Something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const finishExperiment = async () => {
    await endWebGazer();
    const participantId = localStorage.getItem("participant_id");

    window.location.href = `https://sosci.rlp.net/nikhil/?q=qnr2&r=${participantId}`;
  };

  return (
    <div
      className={`min-h-screen ${
        darkMode ? "bg-[#0B1020] text-white" : "bg-white text-black"
      }`}
    >
      <ChatHeader role={role} darkMode={darkMode} setDarkMode={setDarkMode} />

      <main className="max-w-6xl mx-auto px-4 py-6">
        <div
          className={`rounded-3xl border shadow-xl overflow-hidden ${
            darkMode
              ? "bg-[#141B34] border-gray-800"
              : "bg-white border-red-200"
          }`}
        >
          <ChatMessages
            messages={messages}
            loading={loading}
            darkMode={darkMode}
            role={role}
          />

          <ChatInput
            input={input}
            setInput={setInput}
            sendMessage={sendMessage}
            loading={loading}
            darkMode={darkMode}
          />

          <div className="flex justify-center py-4">
            <button
              onClick={() => setShowFinishModal(true)}
              className="
                bg-green-600
                hover:bg-green-700
                text-white
                px-6
                py-2
                rounded-lg
                font-semibold
              "
            >
              Finish Experiment
            </button>
          </div>
        </div>
      </main>

      {showFinishModal && (
        <div
          onClick={() => setShowFinishModal(false)}
          className="
            fixed
            inset-0
            z-50
            flex
            items-center
            justify-center
            bg-black/60
            backdrop-blur-sm
          "
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className={`w-full max-w-md rounded-2xl p-6 shadow-2xl ${
              darkMode
                ? "bg-[#141B34] border border-gray-700"
                : "bg-white border border-gray-200"
            }`}
          >
            <h2 className="text-2xl font-bold mb-4">Finish Experiment?</h2>

            <p
              className={`mb-6 ${darkMode ? "text-gray-300" : "text-gray-600"}`}
            >
              You will be redirected to the post-survey questionnaire. After
              proceeding, you will not be able to continue this chat session.
            </p>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowFinishModal(false)}
                className={`
                  px-4
                  py-2
                  rounded-lg
                  border
                  ${
                    darkMode
                      ? "border-gray-600 hover:bg-gray-800"
                      : "border-gray-300 hover:bg-gray-100"
                  }
                `}
              >
                Continue Chat
              </button>

              <button
                onClick={finishExperiment}
                className="
                  px-4
                  py-2
                  rounded-lg
                  bg-green-600
                  hover:bg-green-700
                  text-white
                "
              >
                Proceed to Survey
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatPage;
