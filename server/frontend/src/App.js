import LoginPanel from "./components/Login/Login";
import { Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<LoginPanel />} />
    </Routes>
  );
}

export default App;