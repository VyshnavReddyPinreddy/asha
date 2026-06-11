import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import ForgotPassword from "./pages/ForgotPassword";
import Assistant from "./pages/Assistant";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Landing />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/forgot-password"
          element={<ForgotPassword />}
        />

        <Route
          path="/assistant"
          element={
            <ProtectedRoute>
              <Assistant />
            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;