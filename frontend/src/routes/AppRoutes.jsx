import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import CropPlanning from "../pages/CropPlanning";
import WeatherRisk from "../pages/WeatherRisk";
import DiseaseDetection from "../pages/DiseaseDetection";
import MarketIntelligence from "../pages/MarketIntelligence";
import Strategist from "../pages/Strategist";
import Login from "../pages/Login";
import Register from "../pages/Register";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
};

const PublicRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  return children;
};

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/crop-planning" element={<ProtectedRoute><CropPlanning /></ProtectedRoute>} />
      <Route path="/weather-risk" element={<ProtectedRoute><WeatherRisk /></ProtectedRoute>} />
      <Route path="/disease-detection" element={<ProtectedRoute><DiseaseDetection /></ProtectedRoute>} />
      <Route path="/market-intelligence" element={<ProtectedRoute><MarketIntelligence /></ProtectedRoute>} />
      <Route path="/strategist" element={<ProtectedRoute><Strategist /></ProtectedRoute>} />
      <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
    </Routes>
  );
}

export default AppRoutes;