import { useEffect } from "react";
import api from "./services/api";

function App() {

  useEffect(() => {

    api.get("health/")
      .then(res => console.log(res.data))
      .catch(err => console.log(err));

  }, []);

  return (
    <>
      <h1>Research Lab AI</h1>
    </>
  );
}

export default App;