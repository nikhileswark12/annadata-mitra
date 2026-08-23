import { Card, CardContent, Typography, Stack } from "@mui/material";

function ForecastCard({ forecast }) {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          5-Day Forecast
        </Typography>

        <Stack spacing={1}>
          {forecast.map((item) => (
            <Typography key={item.day}>
              {item.day}: {item.temp}
            </Typography>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}

export default ForecastCard;