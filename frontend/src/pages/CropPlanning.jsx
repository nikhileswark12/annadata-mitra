import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
  Box,
  Chip,
  Alert
} from "@mui/material";
import BarChartIcon from '@mui/icons-material/BarChart';
import StarIcon from '@mui/icons-material/Star';
import InfoIcon from '@mui/icons-material/Info';
import { getCropRecommendation } from "../services/cropService";
import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import CropSuitabilityChart from "../components/crop/CropSuitabilityChart";

function CropPlanning() {
  const [formData, setFormData] = useState({
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    ph: "",
    rainfall: "",
    temperature: "",
    humidity: "",
    location: "",
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");

    try {
      const parsedData = {
        nitrogen: Number(formData.nitrogen),
        phosphorus: Number(formData.phosphorus),
        potassium: Number(formData.potassium),
        ph: Number(formData.ph),
        rainfall: Number(formData.rainfall),
        temperature: Number(formData.temperature),
        humidity: Number(formData.humidity),
        location: formData.location,
      };

      const response = await getCropRecommendation(parsedData);
      
      if (response.data?.success === true) {
        const mappedResults = response.data.data.recommendations.map(rec => ({
          crop: rec.crop,
          suitability: rec.confidence,
          reason: rec.reasoning,
          icon: rec.icon || "🌱"
        }));
        setResults(mappedResults);
      } else {
        setError("Failed to fetch recommendations.");
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "An error occurred while generating recommendations.");
    } finally {
      setLoading(false);
    }
  };

  const bestCrop = results[0];

  return (
    <Layout>
      <PageHeader
        title="Crop Planning"
        subtitle="Enter soil nutrients and environmental conditions to get intelligent crop recommendations."
      />

      <Grid container spacing={3}>
        {/* LEFT SIDE */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Stack spacing={3}>
            {/* FORM */}
            <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
              <Stack spacing={3}>
                <Typography variant="h5" fontWeight={800}>
                  Soil & Climate Inputs
                </Typography>

                <Grid container spacing={2}>
                  {[
                    { label: "Nitrogen (N)", name: "nitrogen" },
                    { label: "Phosphorus (P)", name: "phosphorus" },
                    { label: "Potassium (K)", name: "potassium" },
                    { label: "pH Level", name: "ph" },
                    { label: "Rainfall (mm)", name: "rainfall" },
                    { label: "Temperature (°C)", name: "temperature" },
                    { label: "Humidity (%)", name: "humidity" },
                    { label: "Location", name: "location" },
                  ].map((field) => (
                    <Grid key={field.name} size={{ xs: 12, sm: 6 }}>
                      <TextField
                        fullWidth
                        label={field.label}
                        name={field.name}
                        value={formData[field.name]}
                        onChange={handleChange}
                      />
                    </Grid>
                  ))}
                </Grid>

                {error && <Alert severity="error">{error}</Alert>}
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading}
                  sx={{
                    borderRadius: 3,
                    fontWeight: 700,
                    backgroundColor: "#2e7d32",
                  }}
                >
                  {loading ? "Generating..." : "Generate Recommendations"}
                </Button>
              </Stack>
            </Paper>

            {/* CHART */}
            {results.length > 0 && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <BarChartIcon fontSize="small" />
                    Suitability Comparison Chart
                  </Box>
                </Typography>

                <CropSuitabilityChart data={results} />
              </Paper>
            )}
          </Stack>
        </Grid>

        {/* RIGHT SIDE */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Stack spacing={3}>
            {/* BEST CROP */}
            {bestCrop && (
              <Paper
                elevation={4}
                sx={{
                  p: 4,
                  borderRadius: 4,
                  backgroundColor: "#e8f5e9",
                }}
              >
                <Typography variant="h6" fontWeight={700} color="#2e7d32">
                  <Box display="flex" alignItems="center" gap={1}>
                    <StarIcon fontSize="small" />
                    Best Crop Recommendation
                  </Box>
                </Typography>

                <Typography variant="h4" fontWeight={800} mt={1}>
                  {bestCrop.icon} {bestCrop.crop}
                </Typography>

                <Chip
                  label={`${bestCrop.suitability}% Match`}
                  color="success"
                  sx={{ mt: 1, fontWeight: 700 }}
                />

                <Typography mt={2} color="text.secondary">
                  {bestCrop.reason}
                </Typography>
              </Paper>
            )}

            {/* COMPARISON */}
            <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
              <Typography variant="h6" fontWeight={800} mb={2}>
                Crop Comparison
              </Typography>

              {results.length > 0 ? (
                <Stack spacing={2}>
                  {results.map((item, index) => (
                    <Paper
                      key={index}
                      variant="outlined"
                      sx={{
                        p: 3,
                        borderRadius: 3,
                        borderColor:
                          index === 0 ? "#66bb6a" : "#e0e0e0",
                        backgroundColor:
                          index === 0 ? "#f1f8e9" : "#fafafa",
                      }}
                    >
                      <Box display="flex" justifyContent="space-between">
                        <Typography fontWeight={700}>
                          {index + 1}. {item.icon} {item.crop}
                        </Typography>

                        <Typography fontWeight={700}>
                          {item.suitability}%
                        </Typography>
                      </Box>

                      <Typography variant="body2" mt={1} color="text.secondary">
                        {item.reason}
                      </Typography>
                    </Paper>
                  ))}
                </Stack>
              ) : (
                <Typography color="text.secondary">
                  Enter data to generate recommendations.
                </Typography>
              )}
            </Paper>

            {/* EXPLANATION */}
            {results.length > 0 && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                      <Box display="flex" alignItems="center" gap={1}>
                        <InfoIcon fontSize="small" />
                        Why this recommendation?
                      </Box>
                    </Typography>

                <Typography variant="body2" color="text.secondary">
                  The system analyzes soil nutrients (NPK), pH level, rainfall,
                  temperature, and humidity to match crops with optimal growing
                  conditions. The top recommendation is selected based on the
                  highest suitability score, ensuring maximum yield potential
                  and reduced risk.
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default CropPlanning;