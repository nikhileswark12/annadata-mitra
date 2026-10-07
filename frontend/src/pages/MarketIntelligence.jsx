import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Box,
  Chip,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import MarketFilterForm from "../components/market/MarketFilterForm";
import MarketRecommendationCard from "../components/market/MarketRecommendationCard";
import MarketPriceTable from "../components/market/MarketPriceTable";
import PriceTrendChart from "../components/market/PriceTrendChart";
import { getMarketInsights } from "../services/marketService";
import ErrorState from "../components/common/ErrorState";
import { ResultLoadingState } from "../components/common/Loader";
import MetricCard from "../components/common/MetricCard";
import EmptyState from "../components/common/EmptyState";

const initialFormData = {
  crop: "",
  quantity: "",
  location: "",
};

function MarketIntelligence() {
  const [formData, setFormData] = useState(initialFormData);
  const [recommendation, setRecommendation] = useState(null);
  const [prices, setPrices] = useState([]);
  const [trends, setTrends] = useState([]);
  const [highlights, setHighlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await getMarketInsights(formData);
      
      const raw = response.data?.data;
      const d = raw?.data || raw;

      if (!d) {
        throw new Error("Invalid response from server.");
      }

      setRecommendation({
        currentPrice: d.currentPrice,
        predictedPrice: d.predictedPrice,
        advice: d.advice,
        totalValue: d.totalValue,
        trendWatch: d.trendWatch,
        demandInsight: d.demandInsight
      });
      
      setPrices(d.markets || []);
      
      const current = d.currentPrice || 0;
      const predicted = d.predictedPrice || 0;
      const diff = (predicted - current) / 4;
      const calculatedTrends = [
        { label: "Today", value: current },
        { label: "Day 2", value: current + diff },
        { label: "Day 3", value: current + diff * 2 },
        { label: "Day 4", value: current + diff * 3 },
        { label: "Day 5", value: predicted },
      ];
      setTrends(calculatedTrends);
      
      setHighlights([
        {
          title: "Demand Insight",
          value: d.demandInsight ? (d.demandInsight.length > 30 ? d.demandInsight.substring(0, 30) + '...' : d.demandInsight) : "N/A",
          note: "Based on current market queries.",
        },
        {
          title: "Trend Watch",
          value: d.trendWatch || "N/A",
          note: "Predicted short-term movement.",
        },
        {
          title: "Farmer Tip",
          value: "Compare Cost",
          note: "Always compare transport cost with final selling advantage.",
        }
      ]);
    } catch (err) {
      console.error("Market insights error:", err);
      setError({
        message: "Failed to load market insights",
        details: err.response?.data?.message || err.message || "Please check your connection and try again."
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData(initialFormData);
    setRecommendation(null);
    setPrices([]);
    setTrends([]);
    setHighlights([]);
    setError(null);
  };

  return (
    <Layout>
      <PageHeader
        title="Market Intelligence"
        subtitle="Compare market prices, trends, and selling opportunities to make smarter mandi decisions."
      />

      <Grid container spacing={3}>
        {highlights.map((item) => (
          <Grid key={item.title} size={{ xs: 12, sm: 6, md: 4 }}>
            <MetricCard 
              title={item.title}
              value={item.value}
              subtitle={item.note}
              color="primary"
            />
          </Grid>
        ))}

        <Grid size={12}>
          <MarketFilterForm
            formData={formData}
            onChange={handleChange}
            onSubmit={handleSubmit}
            onReset={handleReset}
            loading={loading}
          />
        </Grid>

        {error && (
          <Grid size={12}>
            <Box sx={{ pt: 2 }}>
              <ErrorState title={error.message} message={error.details} onRetry={handleSubmit} />
            </Box>
          </Grid>
        )}

        {loading && (
          <Grid size={12}>
            <Box sx={{ pt: 2 }}>
              <ResultLoadingState height={300} message="Analyzing market trends..." />
            </Box>
          </Grid>
        )}

        {!loading && !error && !recommendation && prices.length === 0 && (
          <Grid size={12}>
             <Box sx={{ pt: 2 }}>
                <EmptyState 
                  title="No Analysis Result" 
                  description="Enter your crop, quantity, and location to view available market information."
                />
             </Box>
          </Grid>
        )}

        {!loading && !error && recommendation && (
          <Grid size={{ xs: 12, md: 4 }}>
            <Stack spacing={3} sx={{ height: "100%", pt: 2 }}>
              <MarketRecommendationCard recommendation={recommendation} cropName={formData.crop} />

              <Paper elevation={3} sx={{ p: 3, borderRadius: 4 }}>
                <Stack spacing={2}>
                  <Typography variant="h6" fontWeight={800}>
                    Selling Guidance
                  </Typography>

                  <Chip
                    label="Best Time: Short Wait"
                    sx={{
                      width: "fit-content",
                      fontWeight: 700,
                      backgroundColor: "#e8f5e9",
                      color: "#2e7d32",
                    }}
                  />

                  <Typography variant="body2" color="text.secondary">
                    If storage is available and demand remains strong, waiting briefly may help improve your returns.
                  </Typography>

                  <Typography variant="body2" color="text.secondary">
                    Also compare transport cost before picking a farther market with a slightly better modal price.
                  </Typography>
                </Stack>
              </Paper>
            </Stack>
          </Grid>
        )}

        {!loading && !error && prices.length > 0 && (
          <Grid size={{ xs: 12, md: recommendation ? 8 : 12 }}>
            <Box sx={{ pt: 2 }}>
              <Paper elevation={3} sx={{ p: 3, borderRadius: 4 }}>
                <Stack spacing={2}>
                  <Box>
                    <Typography variant="h6" fontWeight={800}>
                      Market Price Comparison
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Compare available mandi prices and identify the most profitable selling option.
                    </Typography>
                  </Box>

                  <MarketPriceTable prices={prices} cropName={formData.crop} />
                </Stack>
              </Paper>
            </Box>
          </Grid>
        )}

        {!loading && !error && trends.length > 0 && (
          <Grid size={{ xs: 12, md: 8 }}>
            <Box sx={{ pt: 2 }}>
              <Paper elevation={3} sx={{ p: 3, borderRadius: 4 }}>
                <Stack spacing={2}>
                  <Typography variant="h6" fontWeight={800}>
                    Price Trend Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Historical price movement helps estimate whether current market timing is favorable.
                  </Typography>
                  <PriceTrendChart trends={trends} />
                </Stack>
              </Paper>
            </Box>
          </Grid>
        )}

        {!loading && !error && recommendation && (
          <Grid size={{ xs: 12, md: 4 }}>
            <Box sx={{ pt: 2, height: "100%" }}>
              <Paper elevation={3} sx={{ p: 3, borderRadius: 4, height: "100%" }}>
                <Stack spacing={2}>
                      <Typography variant="h6" fontWeight={800}>
                        Smart Market Tips
                      </Typography>

                      {[
                        "Check modal price, not just max price, for realistic selling expectations.",
                        "A nearby mandi with slightly lower price may still be more profitable after transport savings.",
                        "Track trends over multiple days before finalizing large-volume sales.",
                      ].map((tip, index) => (
                        <Paper
                          key={index}
                          variant="outlined"
                          sx={{
                            p: 2,
                            borderRadius: 3,
                            borderColor: "divider",
                            backgroundColor: "background.paper",
                          }}
                        >
                          <Box>
                            <Typography variant="body2">{tip}</Typography>
                          </Box>
                        </Paper>
                      ))}
                </Stack>
              </Paper>
            </Box>
          </Grid>
        )}
      </Grid>
    </Layout>
  );
}

export default MarketIntelligence;