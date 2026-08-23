import { Card, CardContent, Typography } from "@mui/material";

function CropResultCard({ crop, score }) {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {crop}
        </Typography>
        <Typography variant="body1" color="primary">
          Suitability Score: {score}%
        </Typography>
      </CardContent>
    </Card>
  );
}

export default CropResultCard;