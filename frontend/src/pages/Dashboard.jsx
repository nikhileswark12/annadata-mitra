import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Grid from "@mui/material/Grid";
import {
  Box,
  Paper,
  Stack,
  Typography,
  Button,
  Alert,
  AlertTitle
} from "@mui/material";



import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import EmptyState from "../components/common/EmptyState";
import { PageLoadingState } from "../components/common/Loader";
import ErrorState from "../components/common/ErrorState";
import StatusChip from "../components/common/StatusChip";
import api from "../services/api";

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get("/dashboard/stats");
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

  if (error) {
    return (
      <Layout>
        <PageHeader 
          title="Your Agricultural Decision Center" 
          subtitle="Monitor crop conditions, assess risks, explore markets, and get AI-guided recommendations." 
        />
        <ErrorState message={error} onRetry={() => window.location.reload()} />
      </Layout>
    );
  }

  const renderContent = () => {
    if (loading) {
      return <PageLoadingState />;
    }

    const agents = [
      {
        title: "Crop Planning",
        purpose: "Help determine suitable crops based on available soil/environment information.",
        status: data?.cropSuggestions > 0 ? `${data.cropSuggestions} plans created` : "No plans yet",
        action: "Plan a Crop",
        route: "/crop-planning"
      },
      {
        title: "Climate & Risk",
        purpose: "Understand weather conditions and agricultural risks.",
        status: data?.weatherAlerts > 0 ? `${data.weatherAlerts} risk checks done` : "No recent checks",
        action: "Assess Weather Risk",
        route: "/weather-risk"
      },
      {
        title: "Vision Agronomist",
        purpose: "Analyze crop/plant images for potential disease or health issues.",
        status: data?.diseaseScans > 0 ? `${data.diseaseScans} scans completed` : "No scans yet",
        action: "Analyze Crop Image",
        route: "/disease-detection"
      },
      {
        title: "Market Intelligence",
        purpose: "Understand market prices and selling opportunities.",
        status: data?.bestMarketPrice?.price ? `Best price: ₹${data.bestMarketPrice.price} (${data.bestMarketPrice.crop})` : "No market searches",
        action: "Check Market Prices",
        route: "/market-intelligence"
      },
      {
        title: "Strategist",
        purpose: "Combine agricultural intelligence into actionable guidance.",
        status: "Ready for consultation",
        action: "Get Strategic Guidance",
        route: "/strategist"
      }
    ];

    const recentActivities = data?.recentActivities || [];

    return (
      <Grid container spacing={3}>
        {/* System Status */}
        <Grid size={{ xs: 12 }}>
          <Alert severity="info">
            <AlertTitle>System Status</AlertTitle>
            No live agricultural alert is displayed on the dashboard yet. Run a climate check for current weather-risk analysis, or consult the Vision Agronomist if you notice crop issues.
          </Alert>
        </Grid>

        {/* Five-Agent Overview */}
        <Grid size={{ xs: 12 }}>
          <Typography variant="h5" fontWeight={800} gutterBottom sx={{ mt: 2 }}>
            Agricultural Agents
          </Typography>
          <Grid container spacing={2}>
            {agents.map((agent) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={agent.title}>
                <Paper
                  elevation={2}
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                  }}
                >
                  <Box mb={2}>
                    <Typography variant="h6" fontWeight={700}>
                      {agent.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" mb={2} sx={{ flexGrow: 1 }}>
                    {agent.purpose}
                  </Typography>
                  <Box mb={2}>
                    <StatusChip status="inactive" label={agent.status} size="small" />
                  </Box>
                  <Button
                    component={Link}
                    to={agent.route}
                    variant="outlined"
                    fullWidth
                    sx={{ textTransform: "none", fontWeight: 700 }}
                  >
                    {agent.action}
                  </Button>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Strategist Preview */}
        <Grid size={{ xs: 12, md: 8 }}>
          <Typography variant="h5" fontWeight={800} gutterBottom sx={{ mt: 2 }}>
            Your Next Steps
          </Typography>
          <EmptyState
            title="No recent strategic guidance"
            description="Consult the Strategist for personalized advice and actionable guidance."
            action={
              <Button component={Link} to="/strategist" variant="contained" color="primary">
                Get Strategic Guidance
              </Button>
            }
          />
        </Grid>

        {/* Recent Activity */}
        <Grid size={{ xs: 12, md: 4 }}>
          <Typography variant="h5" fontWeight={800} gutterBottom sx={{ mt: 2 }}>
            Recent Activity
          </Typography>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 3, height: "100%", minHeight: 250 }}>
            {recentActivities.length > 0 ? (
              <Stack spacing={2}>
                {recentActivities.map((activity, index) => (
                  <Paper
                    key={index}
                    variant="outlined"
                    sx={{
                      p: 2,
                      borderRadius: 2,
                      borderColor: "divider",
                      backgroundColor: "background.default",
                    }}
                  >
                    <Typography variant="body2">
                      {activity.text}{" "}
                      {activity.time && `(${new Date(activity.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })})`}
                    </Typography>
                  </Paper>
                ))}
              </Stack>
            ) : (
              <EmptyState 
                title="No activity yet"
                description="Your recent actions will appear here."
              />
            )}
          </Paper>
        </Grid>
      </Grid>
    );
  };

  return (
    <Layout>
      <PageHeader
        title="Your Agricultural Decision Center"
        subtitle="Monitor crop conditions, assess risks, explore markets, and get AI-guided recommendations."
      />
      {renderContent()}
    </Layout>
  );
}

export default Dashboard;