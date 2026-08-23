import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Paper,
  Stack,
  Typography,
  TextField,
  Button,
  Chip,
} from "@mui/material";
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ScheduleIcon from '@mui/icons-material/Schedule';
import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import { getUnifiedGuidance } from "../services/strategistService";
import Alert from "@mui/material/Alert";

function Strategist() {
  const [goal, setGoal] = useState("");
  const [plan, setPlan] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGeneratePlan = async () => {
    if (!goal) return;

    setLoading(true);
    setError("");

    try {
      const response = await getUnifiedGuidance({ goal });
      if (response.data?.success === true) {
        setPlan(response.data.data);
      } else {
        setError("Failed to generate strategy.");
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "An error occurred while generating strategy.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <PageHeader
        title="Strategist"
        subtitle="Use AI-backed guidance to create smarter crop, market, and risk planning strategies."
      />

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Typography variant="h5" fontWeight={800}>
                Planning Goal
              </Typography>

              <TextField
                fullWidth
                multiline
                minRows={5}
                label="Enter your farming goal"
                placeholder="Example: I want to improve profit this season while reducing crop disease and weather risk."
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
              />

              {error && <Alert severity="error">{error}</Alert>}
              <Button
                variant="contained"
                onClick={handleGeneratePlan}
                disabled={loading || !goal}
                sx={{
                  width: "fit-content",
                  px: 4,
                  py: 1.2,
                  borderRadius: 3,
                  textTransform: "none",
                  fontWeight: 700,
                  backgroundColor: "#2e7d32",
                }}
              >
                {loading ? "Generating..." : "Generate Strategy"}
              </Button>
            </Stack>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Typography variant="h5" fontWeight={800}>
                Strategy Output
              </Typography>

              {plan ? (
                <>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label={`Crop: ${plan.crop || "N/A"}`} color="success" />
                    <Chip label={`Season: ${plan.season || "N/A"}`} variant="outlined" />
                    <Chip label={`Confidence: ${plan.confidence || 0}%`} color="primary" />
                  </Stack>

                  <Paper
                    variant="outlined"
                    sx={{
                      p: 3,
                      borderRadius: 3,
                      backgroundColor: "#f8fff8",
                      borderColor: "#c8e6c9",
                    }}
                  >
                    <Typography variant="h6" fontWeight={700} mb={2}>
                      Strategic Suggestions
                    </Typography>
                    <Stack spacing={2}>
                      <Box display="flex" gap={1} alignItems="flex-start">
                        <CheckCircleOutlineIcon fontSize="small" sx={{ mt: 0.6 }} />
                        <Typography variant="body2"><strong>Crop Advice:</strong> {plan.cropAdvice}</Typography>
                      </Box>
                      <Box display="flex" gap={1} alignItems="flex-start">
                        <CheckCircleOutlineIcon fontSize="small" sx={{ mt: 0.6 }} />
                        <Typography variant="body2"><strong>Market Timing:</strong> {plan.marketTiming}</Typography>
                      </Box>
                      <Box display="flex" gap={1} alignItems="flex-start">
                        <CheckCircleOutlineIcon fontSize="small" sx={{ mt: 0.6 }} />
                        <Typography variant="body2"><strong>Weather Risk:</strong> {plan.weatherRisk}</Typography>
                      </Box>
                      <Box display="flex" gap={1} alignItems="flex-start">
                        <CheckCircleOutlineIcon fontSize="small" sx={{ mt: 0.6 }} />
                        <Typography variant="body2"><strong>Farm Advisory:</strong> {plan.farmAdvisory}</Typography>
                      </Box>
                    </Stack>
                  </Paper>

                  <Paper
                    variant="outlined"
                    sx={{
                      p: 3,
                      borderRadius: 3,
                      backgroundColor: "#fcfcff",
                    }}
                  >
                    <Typography variant="h6" fontWeight={700} mb={2}>
                      Action Timeline
                    </Typography>
                    <Stack spacing={1}>
                      {plan.actions && plan.actions.map((item, index) => (
                        <Box key={index} display="flex" gap={1} alignItems="flex-start">
                          <ScheduleIcon fontSize="small" sx={{ mt: 0.3 }} />
                          <Typography variant="body2">{item}</Typography>
                        </Box>
                      ))}
                    </Stack>
                  </Paper>
                </>
              ) : (
                <Typography color="text.secondary">
                  Enter a goal and generate an AI strategy plan. Your personalized farming guidance will appear here.
                </Typography>
              )}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default Strategist;