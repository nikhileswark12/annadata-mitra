import { Card, CardContent, Typography, Chip, Stack } from "@mui/material";

function MarketRecommendationCard({ recommendation, cropName }) {
  if (!recommendation) return null;

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Market Insights
        </Typography>

        <Stack spacing={1.5}>
          <Typography>
            <strong>Crop:</strong> {cropName || "Unknown"}
          </Typography>
          <Typography>
            <strong>Current Price:</strong> ₹{recommendation.currentPrice}/quintal
          </Typography>
          <Typography>
            <strong>Predicted Price:</strong> ₹{recommendation.predictedPrice}/quintal
          </Typography>
          {recommendation.totalValue > 0 && (
            <Typography>
              <strong>Total Value:</strong> ₹{recommendation.totalValue}
            </Typography>
          )}
          <Typography>
            <strong>Advice:</strong> {recommendation.advice}
          </Typography>

          <Chip
            label={`Trend: ${recommendation.trendWatch}`}
            color={recommendation.trendWatch === "Upward" || recommendation.trendWatch === "Up" ? "success" : recommendation.trendWatch === "Stable" ? "default" : "warning"}
            sx={{ width: "fit-content", fontWeight: 600 }}
          />
        </Stack>
      </CardContent>
    </Card>
  );
}

export default MarketRecommendationCard;