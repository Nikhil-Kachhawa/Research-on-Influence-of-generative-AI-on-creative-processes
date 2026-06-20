import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000/api/",
});

export default api;

export const getChatHistory = async (sessionId) => {
  const response = await api.get(
    `chat-history/${sessionId}/`
  );

  return response.data;
};

export const getDashboardData = async () => {
  const response = await api.get(
    "dashboard-data/"
  );

  return response.data;
};