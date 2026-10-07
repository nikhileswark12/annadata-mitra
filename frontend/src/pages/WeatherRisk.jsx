import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
  Alert,
  AlertTitle,
  Box
} from "@mui/material";

import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import { getRiskAssessment } from "../services/weatherService";
import AIResultCard from "../components/common/AIResultCard";
import EmptyState from "../components/common/EmptyState";
import { ResultLoadingState } from "../components/common/Loader";
import ErrorState from "../components/common/ErrorState";
import MetricCard from "../components/common/MetricCard";
import SectionHeader from "../components/common/SectionHeader";
import StatusChip from "../components/common/StatusChip";

function WeatherRisk() {
  const [location, setLocation] = useState("");
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");

  const handleFetch = async (e) => {
    if (e) e.preventDefault();
    const trimmedLocation = location.trim();
    
    if (!trimmedLocation) {
      setFormError("Location is required");
      return;
    }

    setFormError("");
    setLoading(true);
    setError("");
    setWeather(null);

    try {
      const response = await getRiskAssessment({ location: trimmedLocation });
      if (response.data?.success === true) {
        setWeather(response.data.data);
      } else {
        setError("Failed to fetch weather risk data.");
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || err.message || "An error occurred while fetching weather data.");
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "high": return "error";
      case "medium": return "warning";
      case "low": return "info";
      default: return "info";
    }
  };

  const handleChange = (e) => {
    setLocation(e.target.value);
    if (formError) setFormError("");
  };

  return (
    <Layout>
      <PageHeader
        title="Climate & Risk"
        subtitle="Analyze weather conditions and identify potential agricultural risks."
      />

      <Grid container spacing={4}>
        {/* LEFT SIDE - LOCATION INPUT */}
        <Grid item xs={12} md={5}>
          <Paper elevation={0} sx={{ p: 4, borderRadius: 3, border: "1px solid #e0e0e0" }}>
            <form onSubmit={handleFetch}>
              <Stack spacing={3}>
                <SectionHeader title="Location Input" />

                <TextField
                  label="Enter Location"
                  placeholder="e.g. Pune, Maharashtra"
                  value={location}
                  onChange={handleChange}
                  error={!!formError}
                  helperText={formError || "Enter a city, region, or state"}
                  fullWidth
                  disabled={loading}
                />

                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  sx={{
                    borderRadius: 2,
                    fontWeight: 700,
                    textTransform: "none",
                    py: 1.5,
                  }}
                >
                  {loading ? "Assessing..." : "Assess Weather Risk"}
                </Button>
              </Stack>
            </form>
          </Paper>
        </Grid>

        {/* RIGHT SIDE - RESULTS OR STATES */}
        <Grid item xs={12} md={7}>
          {loading && <ResultLoadingState height={400} />}

          {!loading && error && (
            <ErrorState
              title="Assessment Failed"
              message={error}
              onRetry={handleFetch}
            />
          )}

          {!loading && !error && !weather && (
            <EmptyState
              title="No Weather Data"
              description="Enter your location to assess current weather conditions and agricultural risks."
            />
          )}

          {!loading && !error && weather && (
            <Stack spacing={4}>
              
              {/* CURRENT WEATHER METRICS */}
              <Box>
                <SectionHeader title="Current Conditions" />
                <Grid container spacing={2}>
                  <Grid item xs={6} sm={4}>
                    <MetricCard 
                      title="Temperature" 
                      value={`${weather.temperature}°C`} 
                    />
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <MetricCard 
                      title="Humidity" 
                      value={`${weather.humidity}%`} 
                    />
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <MetricCard 
                      title="Rainfall" 
                      value={`${weather.rainfall} mm`} 
                    />
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <MetricCard 
                      title="Wind Speed" 
                      value={`${weather.windSpeed || 0} km/h`} 
                    />
                  </Grid>
                  <Grid item xs={12} sm={8}>
                    <MetricCard 
                      title="Condition" 
                      value={weather.condition} 
                    />
                  </Grid>
                </Grid>
              </Box>

              {/* RISK ALERTS & ADVISORY */}
              <AIResultCard
                title="Agricultural Risks & Advisory"
                primaryResult={weather.risks && weather.risks.length > 0 ? `${weather.risks.length} Alert(s)` : "Normal"}
                severity={weather.risks && weather.risks.length > 0 ? weather.risks[0].severity : "Low"}
              >
                <Stack spacing={2} mt={2}>
                  {weather.risks && weather.risks.length > 0 ? (
                    weather.risks.map((risk, index) => (
                      <Alert key={index} severity={getSeverityColor(risk.severity)}>
                        <AlertTitle sx={{ fontWeight: 700 }}>{risk.type}</AlertTitle>
                        <Typography variant="body2" gutterBottom>
                          {risk.message}
                        </Typography>
                        {risk.recommendation && (
                          <Typography variant="caption" display="block" sx={{ mt: 1, p: 1, bgcolor: 'rgba(255,255,255,0.5)', borderRadius: 1 }}>
                            <strong>Recommendation:</strong> {risk.recommendation}
                          </Typography>
                        )}
                      </Alert>
                    ))
                  ) : (
                    <Box display="flex" alignItems="center" gap={2} p={2} sx={{ bgcolor: 'success.50', borderRadius: 2 }}>
                      <StatusChip status="Optimal" />
                      <Typography variant="body2" color="success.800">
                        No major agricultural risks identified for current weather conditions.
                      </Typography>
                    </Box>
                  )}
                </Stack>
              </AIResultCard>

            </Stack>
          )}
        </Grid>
      </Grid>
    </Layout>
  );
}

export default WeatherRisk;