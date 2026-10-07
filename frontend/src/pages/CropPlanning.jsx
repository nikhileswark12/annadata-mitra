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

import { getCropRecommendation } from "../services/cropService";
import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import CropSuitabilityChart from "../components/crop/CropSuitabilityChart";
import AIResultCard from "../components/common/AIResultCard";
import EmptyState from "../components/common/EmptyState";
import { ResultLoadingState } from "../components/common/Loader";
import ErrorState from "../components/common/ErrorState";

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
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
    if (formErrors[e.target.name]) {
      setFormErrors((prev) => ({ ...prev, [e.target.name]: undefined }));
    }
  };

  const validate = () => {
    const errors = {};
    const { nitrogen, phosphorus, potassium, ph, rainfall, temperature, humidity } = formData;

    if (!nitrogen) errors.nitrogen = "Required";
    else if (Number(nitrogen) < 0) errors.nitrogen = "Cannot be negative";

    if (!phosphorus) errors.phosphorus = "Required";
    else if (Number(phosphorus) < 0) errors.phosphorus = "Cannot be negative";

    if (!potassium) errors.potassium = "Required";
    else if (Number(potassium) < 0) errors.potassium = "Cannot be negative";

    if (!ph) errors.ph = "Required";
    else if (Number(ph) < 0 || Number(ph) > 14) errors.ph = "Must be between 0 and 14";

    if (!temperature) errors.temperature = "Required";

    if (!humidity) errors.humidity = "Required";
    else if (Number(humidity) < 0 || Number(humidity) > 100) errors.humidity = "Must be between 0 and 100";

    if (!rainfall) errors.rainfall = "Required";
    else if (Number(rainfall) < 0) errors.rainfall = "Cannot be negative";

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;
    
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
          reason: rec.reasoning
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
                <Typography variant="h5" fontWeight={800} gutterBottom>
                  Soil & Climate Inputs
                </Typography>

                <Box>
                  <Typography variant="subtitle1" fontWeight={700} color="primary.main" gutterBottom>
                    Soil Conditions
                  </Typography>
                  <Grid container spacing={2}>
                    {[
                      { label: "Nitrogen (N)", name: "nitrogen" },
                      { label: "Phosphorus (P)", name: "phosphorus" },
                      { label: "Potassium (K)", name: "potassium" },
                      { label: "pH Level", name: "ph" },
                    ].map((field) => (
                      <Grid key={field.name} size={{ xs: 12, sm: 6 }}>
                        <TextField
                          fullWidth
                          label={field.label}
                          name={field.name}
                          type="number"
                          value={formData[field.name]}
                          onChange={handleChange}
                          error={!!formErrors[field.name]}
                          helperText={formErrors[field.name]}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </Box>

                <Box>
                  <Typography variant="subtitle1" fontWeight={700} color="primary.main" gutterBottom>
                    Climate Conditions
                  </Typography>
                  <Grid container spacing={2}>
                    {[
                      { label: "Temperature (°C)", name: "temperature" },
                      { label: "Humidity (%)", name: "humidity" },
                      { label: "Rainfall (mm)", name: "rainfall" },
                    ].map((field) => (
                      <Grid key={field.name} size={{ xs: 12, sm: 4 }}>
                        <TextField
                          fullWidth
                          label={field.label}
                          name={field.name}
                          type="number"
                          value={formData[field.name]}
                          onChange={handleChange}
                          error={!!formErrors[field.name]}
                          helperText={formErrors[field.name]}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </Box>

                <Box>
                  <Typography variant="subtitle1" fontWeight={700} color="primary.main" gutterBottom>
                    Location
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid size={{ xs: 12 }}>
                      <TextField
                        fullWidth
                        label="Location (Optional)"
                        name="location"
                        value={formData.location}
                        onChange={handleChange}
                      />
                    </Grid>
                  </Grid>
                </Box>
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
            {loading ? (
              <ResultLoadingState height={400} />
            ) : results.length > 0 ? (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  Suitability Comparison Chart
                </Typography>

                <CropSuitabilityChart data={results} />
              </Paper>
            ) : null}
          </Stack>
        </Grid>

        {/* RIGHT SIDE */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Stack spacing={3}>
            {loading ? (
              <ResultLoadingState height={200} />
            ) : error ? (
              <ErrorState message={error} onRetry={handleSubmit} />
            ) : bestCrop ? (
              <AIResultCard
                title="Best Crop Recommendation"
                primaryResult={bestCrop.crop}
                confidence={bestCrop.suitability}
                explanation={bestCrop.reason}
              />
            ) : (
              <EmptyState 
                title="No Recommendation Yet" 
                description="Enter your soil and climate details and click generate to receive an AI-powered crop recommendation." 
              />
            )}

            {/* COMPARISON */}
            {results.length > 0 && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  Crop Comparison
                </Typography>

                <Stack spacing={2}>
                  {results.map((item, index) => (
                    <Paper
                      key={index}
                      variant="outlined"
                      sx={{
                        p: 3,
                        borderRadius: 3,
                        borderColor: index === 0 ? "primary.main" : "divider",
                        backgroundColor: index === 0 ? "success.light" : "background.paper",
                      }}
                    >
                      <Box display="flex" justifyContent="space-between">
                        <Typography fontWeight={700}>
                          {index + 1}. {item.crop}
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
              </Paper>
            )}

            {/* EXPLANATION */}
            {results.length > 0 && (
              <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                <Typography variant="h6" fontWeight={800} mb={2}>
                  Why this recommendation?
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