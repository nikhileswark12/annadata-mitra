import { Card, CardContent, Typography, Chip, Stack } from "@mui/material";

function MarketRecommendationCard({ recommendation }) {
  if (!recommendation) return null;

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Best Market Recommendation
        </Typography>

        <Stack spacing={1.5}>
          <Typography>Predicted Price: ₹{recommendation.predictedPrice}</Typography>
          <Typography>
            <strong>Market:</strong> {recommendation.market}
          </Typography>
          <Typography>
            <strong>Crop:</strong> {recommendation.crop}
          </Typography>
          <Typography>
            <strong>Expected Price:</strong> ₹{recommendation.expectedPrice}/quintal
          </Typography>
          <Typography>
            <strong>Reason:</strong> {recommendation.reason}
          </Typography>

          <Chip
            label={recommendation.trend}
            color={recommendation.trend === "Rising" ? "success" : "warning"}
            sx={{ width: "fit-content", fontWeight: 600 }}
          />
        </Stack>
      </CardContent>
    </Card>
  );
}

export default MarketRecommendationCard;