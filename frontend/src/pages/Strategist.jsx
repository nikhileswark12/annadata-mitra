import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Box,
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
} from "@mui/material";

import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import { getUnifiedGuidance } from "../services/strategistService";
import ErrorState from "../components/common/ErrorState";
import { ResultLoadingState } from "../components/common/Loader";
import AIResultCard from "../components/common/AIResultCard";
import EmptyState from "../components/common/EmptyState";

const initialFormData = {
  goal: "",
  crop: "",
  location: "",
};

function Strategist() {
  const [formData, setFormData] = useState(initialFormData);
  const [plan, setPlan] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleGeneratePlan = async () => {
    const trimmedGoal = formData.goal.trim();
    if (!trimmedGoal) return;

    setLoading(true);
    setError(null);
    setPlan(null);

    try {
      // Send the full form data to the backend
      const response = await getUnifiedGuidance({
        goal: trimmedGoal,
        crop: formData.crop.trim(),
        location: formData.location.trim(),
      });
      
      if (response.data?.success === true) {
        setPlan(response.data.data);
      } else {
        setError({ message: "Failed to generate strategy." });
      }
    } catch (err) {
      console.error(err);
      setError({
        message: "An error occurred while generating strategy.",
        details: err.response?.data?.message || err.message || "Please check your connection."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <PageHeader
        title="Strategist"
        subtitle="Synthesize agricultural insights into a unified, actionable farming strategy."
      />

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Typography variant="h6" fontWeight={800}>
                Planning Objective
              </Typography>

              <TextField
                fullWidth
                multiline
                minRows={4}
                label="Enter your farming goal"
                name="goal"
                placeholder="Example: I want to decide what to do with my wheat crop this week."
                value={formData.goal}
                onChange={handleChange}
                disabled={loading}
              />
              
              <TextField
                fullWidth
                label="Target Crop (Optional)"
                name="crop"
                placeholder="e.g., Wheat"
                value={formData.crop}
                onChange={handleChange}
                disabled={loading}
              />

              <TextField
                fullWidth
                label="Location (Optional)"
                name="location"
                placeholder="e.g., Pune"
                value={formData.location}
                onChange={handleChange}
                disabled={loading}
              />

              {error && <ErrorState title={error.message} message={error.details} onRetry={handleGeneratePlan} />}
              
              <Button
                variant="contained"
                onClick={handleGeneratePlan}
                disabled={loading || !formData.goal.trim()}
                sx={{
                  width: "100%",
                  py: 1.2,
                  borderRadius: 3,
                  textTransform: "none",
                  fontWeight: 700,
                  backgroundColor: "#2e7d32",
                }}
              >
                {loading ? "Generating..." : "Generate Guidance"}
              </Button>
            </Stack>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Stack spacing={3} sx={{ height: "100%" }}>
            {loading && (
              <Box sx={{ pt: 2 }}>
                <ResultLoadingState height={400} message="Synthesizing agricultural intelligence..." />
              </Box>
            )}
            
            {!loading && !plan && !error && (
              <Box sx={{ pt: 2, height: "100%" }}>
                <EmptyState 
                  title="Strategist Dashboard" 
                  description="Describe what you want to decide, and Annadata Mitra will organize the available agricultural insights into practical next steps." 
                />
              </Box>
            )}

            {!loading && plan && (
              <AIResultCard
                title="Unified Strategy Guidance"
                primaryResult={plan.explanation?.what || "Integrated Strategy Generated"}
                confidence={plan.confidence || 0}
                explanation={plan.explanation?.why || ""}
              >
                {/* Actions Section */}
                {plan.actions && plan.actions.length > 0 && (
                  <Paper
                    elevation={0}
                    variant="outlined"
                    sx={{
                      p: 3,
                      borderRadius: 3,
                      backgroundColor: "#f8fff8",
                      borderColor: "#c8e6c9",
                      mt: 3
                    }}
                  >
                    <Typography variant="h6" fontWeight={700} mb={2}>
                      Actionable Next Steps
                    </Typography>
                    <Stack spacing={2}>
                      {plan.actions.map((actionText, index) => (
                        <Box key={index} sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                          <Typography variant="body1" sx={{ fontWeight: 800, color: "#2e7d32" }}>
                            •
                          </Typography>
                          <Typography variant="body1" fontWeight={600}>
                            {actionText}
                          </Typography>
                        </Box>
                      ))}
                    </Stack>
                  </Paper>
                )}

                {/* Supporting Context Section */}
                <Paper
                  elevation={0}
                  variant="outlined"
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    backgroundColor: "background.paper",
                    borderColor: "divider",
                    mt: 3
                  }}
                >
                  <Typography variant="h6" fontWeight={700} mb={2}>
                    Supporting Context
                  </Typography>
                  <Stack spacing={2}>
                    {plan.cropAdvice && (
                      <Box>
                        <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>
                          CROP ADVICE
                        </Typography>
                        <Typography variant="body2">{plan.cropAdvice}</Typography>
                      </Box>
                    )}
                    {plan.weatherRisk && (
                      <Box>
                        <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>
                          WEATHER RISK
                        </Typography>
                        <Typography variant="body2">{plan.weatherRisk}</Typography>
                      </Box>
                    )}
                    {plan.marketTiming && (
                      <Box>
                        <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>
                          MARKET TIMING
                        </Typography>
                        <Typography variant="body2">{plan.marketTiming}</Typography>
                      </Box>
                    )}
                    {plan.farmAdvisory && (
                      <Box>
                        <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>
                          FARM ADVISORY
                        </Typography>
                        <Typography variant="body2">{plan.farmAdvisory}</Typography>
                      </Box>
                    )}
                  </Stack>
                </Paper>
                
                {/* Methodology Factors */}
                {plan.explanation?.factors && plan.explanation.factors.length > 0 && (
                   <Box sx={{ mt: 3 }}>
                     <Typography variant="caption" color="text.secondary" fontWeight={600} display="block" gutterBottom>
                        ANALYSIS FACTORS:
                     </Typography>
                     <ul style={{ margin: 0, paddingLeft: 20 }}>
                       {plan.explanation.factors.map((factor, idx) => (
                         <li key={idx}>
                           <Typography variant="caption" color="text.secondary">
                             {factor}
                           </Typography>
                         </li>
                       ))}
                     </ul>
                   </Box>
                )}
              </AIResultCard>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default Strategist;