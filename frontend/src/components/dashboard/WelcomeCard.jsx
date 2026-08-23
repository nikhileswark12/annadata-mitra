import { Card, CardContent, Typography } from "@mui/material";

function WelcomeCard() {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h5" color="primary" gutterBottom>
          Welcome to Annadata Mitra
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Your smart farming assistant for crop planning, weather awareness,
          and agricultural decision support.
        </Typography>
      </CardContent>
    </Card>
  );
}

export default WelcomeCard;