import { useState, useEffect } from "react";
import Grid from "@mui/material/Grid";
import {
  Box,
  Paper,
  Stack,
  Typography,
  Chip,
  Button,
  CircularProgress,
  Alert
} from "@mui/material";
import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import api from "../services/api";

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get("/api/dashboard/stats");
        if (response.data?.success === true) {
          setData(response.data.data);
        } else {
          setError("Failed to fetch dashboard stats.");
        }
      } catch (err) {
        setError(err.message || "Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <Layout>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
          <CircularProgress color="success" />
        </Box>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">{error}</Alert>
        </Box>
      </Layout>
    );
  }

  const summaryCards = data ? [
    {
      title: "Crop Suggestions",
      value: data.cropSuggestions,
      subtitle: "AI-based recommendations generated",
    },
    {
      title: "Weather Alerts",
      value: data.weatherAlerts,
      subtitle: "Potential agricultural risks today",
    },
    {
      title: "Disease Scans",
      value: data.diseaseScans,
      subtitle: "Recent crop image analyses completed",
    },
    {
      title: "Best Market Price",
      value: `₹${data.bestMarketPrice?.price || 0}`,
      subtitle: `Top ${data.bestMarketPrice?.crop || ''} price from ${data.bestMarketPrice?.location || ''}`,
    },
  ] : [];

  const recommendations = data ? [
    {
      title: "Best Crop Window",
      description: data.todaysRecommendations?.cropWindow,
    },
    {
      title: "Market Insight",
      description: data.todaysRecommendations?.marketInsight,
    },
    {
      title: "Farm Advisory",
      description: data.todaysRecommendations?.farmAdvisory,
    },
  ] : [];

  const recentActivities = data?.recentActivities || [];
  return (
    <Layout>
      <PageHeader
        title="Dashboard"
        subtitle="Welcome to Annadata Mitra. Monitor crop planning, market trends, weather risk, and disease detection from one place."
      />

      <Grid container spacing={3}>
        {summaryCards.map((card) => (
          <Grid key={card.title} size={{ xs: 12, sm: 6, md: 3 }}>
            <Paper
              elevation={3}
              sx={{
                p: 3,
                borderRadius: 4,
                height: "100%",
              }}
            >
              <Stack spacing={1}>
                <Typography variant="subtitle1" fontWeight={700} color="#1b5e20">
                  {card.title}
                </Typography>
                <Typography variant="h4" fontWeight={800}>
                  {card.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {card.subtitle}
                </Typography>
              </Stack>
            </Paper>
          </Grid>
        ))}

        <Grid size={{ xs: 12, md: 8 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Box>
                <Typography variant="h5" fontWeight={800} gutterBottom>
                  Today’s Recommendations
                </Typography>
                <Typography color="text.secondary">
                  Smart suggestions generated from your farming support modules.
                </Typography>
              </Box>

              <Grid container spacing={2}>
                {recommendations.map((item) => (
                  <Grid key={item.title} size={{ xs: 12, md: 4 }}>
                    <Paper
                      variant="outlined"
                      sx={{
                        p: 3,
                        borderRadius: 3,
                        height: "100%",
                        borderColor: "#c8e6c9",
                        backgroundColor: "#f8fff8",
                      }}
                    >
                      <Typography variant="h6" fontWeight={700} color="#2e7d32" mb={1}>
                        {item.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {item.description}
                      </Typography>
                    </Paper>
                  </Grid>
                ))}
              </Grid>

              <Box>
                <Button
                  variant="contained"
                  sx={{
                    borderRadius: 3,
                    textTransform: "none",
                    fontWeight: 700,
                    px: 3,
                    backgroundColor: "#2e7d32",
                  }}
                >
                  Explore Insights
                </Button>
              </Box>
            </Stack>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={2}>
              <Typography variant="h5" fontWeight={800}>
                Recent Activity
              </Typography>

              {recentActivities.map((activity, index) => (
                <Paper
                  key={index}
                  variant="outlined"
                  sx={{
                    p: 2,
                    borderRadius: 3,
                    borderColor: "#dcedc8",
                    backgroundColor: "#fcfff9",
                  }}
                >
                  <Typography variant="body2">{activity.text} {activity.time ? `(${new Date(activity.time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})})` : ''}</Typography>
                </Paper>
              ))}

              <Chip
                label="System Status: Active"
                sx={{
                  width: "fit-content",
                  fontWeight: 700,
                  backgroundColor: "#e8f5e9",
                  color: "#2e7d32",
                }}
              />
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default Dashboard;