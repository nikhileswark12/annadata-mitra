import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
  Chip,
  Box,
  Alert,
  AlertTitle
} from "@mui/material";
import CloudIcon from '@mui/icons-material/Cloud';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import DateRangeIcon from '@mui/icons-material/DateRange';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import { getRiskAssessment } from "../services/weatherService";

function WeatherRisk() {
  const [location, setLocation] = useState("");
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFetch = async () => {
    if (!location) return;
    setLoading(true);
    setError("");
    setWeather(null);

    try {
      const response = await getRiskAssessment({ location });
      if (response.data?.success === true) {
        setWeather(response.data.data);
      } else {
        setError("Failed to fetch weather risk data.");
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "An error occurred while fetching weather data.");
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "High": return "error";
      case "Medium": return "warning";
      case "Low": return "info";
      default: return "info";
    }
  };

  return (
    <Layout>
      <PageHeader
        title="Weather Risk"
        subtitle="Analyze weather conditions and identify potential agricultural risks."
      />

      <Grid container spacing={3}>
        {/* LEFT SIDE */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Stack spacing={3}>
            {/* INPUT */}
            <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
              <Stack spacing={2}>
                <Typography variant="h6" fontWeight={800}>
                  Location Input
                </Typography>

                <TextField
                  label="Enter Location"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  fullWidth
                />

                {error && <Alert severity="error">{error}</Alert>}
                <Button
                  variant="contained"
                  onClick={handleFetch}
                  disabled={loading}
                  sx={{
                    borderRadius: 3,
                    fontWeight: 700,
                    backgroundColor: "#2e7d32",
                  }}
                >
                  {loading ? "Checking..." : "Check Weather Risk"}
                </Button>
              </Stack>
            </Paper>

            {/* CURRENT WEATHER */}
            {weather && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <CloudIcon fontSize="small" />
                    Current Weather
                  </Box>
                </Typography>

                <Stack spacing={1}>
                  <Typography>Temperature: {weather.temperature}°C</Typography>
                  <Typography>Humidity: {weather.humidity}%</Typography>
                  <Typography>Rainfall: {weather.rainfall} mm</Typography>
                  <Typography>Condition: {weather.condition}</Typography>
                </Stack>
              </Paper>
            )}
          </Stack>
        </Grid>

        {/* RIGHT SIDE */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Stack spacing={3}>
            {/* RISKS */}
            {weather && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <WarningAmberIcon fontSize="small" />
                    Risk Alerts
                  </Box>
                </Typography>

                <Stack spacing={2}>
                  {weather.risks && weather.risks.map((risk, index) => (
                    <Alert key={index} severity={getSeverityColor(risk.severity)}>
                      <AlertTitle>{risk.type}</AlertTitle>
                      <Typography variant="body2" gutterBottom>
                        {risk.message}
                      </Typography>
                      <Typography variant="caption">
                        <strong>Recommendation:</strong> {risk.recommendation}
                      </Typography>
                    </Alert>
                  ))}
                  {(!weather.risks || weather.risks.length === 0) && (
                    <Typography color="text.secondary">No major risks identified.</Typography>
                  )}
                </Stack>
              </Paper>
            )}



            {/* ADVISORY */}
            {weather && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <LightbulbIcon fontSize="small" />
                    Advisory
                  </Box>
                </Typography>

                <Typography variant="body2" color="text.secondary">
                  Based on current conditions, ensure proper irrigation
                  management and monitor pest activity. High humidity and
                  rainfall may increase disease risk. Adjust farming practices
                  accordingly.
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default WeatherRisk;