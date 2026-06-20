import { useEffect, useState } from "react";
import { getDashboardData } from "../services/api";

function DashboardPage() {

  const [stats, setStats] = useState(null);

  useEffect(() => {

    const loadData = async () => {
      const data = await getDashboardData();
      setStats(data);
    };

    loadData();

  }, []);

  if (!stats) {
    return (
      <div className="p-8">
        Loading...
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-8">

      <h1 className="text-3xl font-bold mb-8">
        Research Dashboard
      </h1>

      <div className="grid md:grid-cols-3 gap-6">

        <div className="border rounded-xl p-6">
          <h2>Total Participants</h2>
          <p className="text-3xl font-bold">
            {stats.participants}
          </p>
        </div>

        <div className="border rounded-xl p-6">
          <h2>Completed</h2>
          <p className="text-3xl font-bold">
            {stats.completed}
          </p>
        </div>

        <div className="border rounded-xl p-6">
          <h2>Average Duration</h2>
          <p className="text-3xl font-bold">
            {stats.avg_duration} min
          </p>
        </div>

        <div className="border rounded-xl p-6">
          <h2>Idea Generator</h2>
          <p className="text-3xl font-bold">
            {stats.idea_generator}
          </p>
        </div>

        <div className="border rounded-xl p-6">
          <h2>Critical Evaluator</h2>
          <p className="text-3xl font-bold">
            {stats.critical_evaluator}
          </p>
        </div>

        <div className="border rounded-xl p-6">
          <h2>Avg Messages</h2>
          <p className="text-3xl font-bold">
            {stats.avg_messages}
          </p>
        </div>

      </div>

    </div>
  );
}

export default DashboardPage;