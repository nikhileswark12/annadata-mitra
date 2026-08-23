import { Card, CardContent, Typography, Stack } from "@mui/material";

function CurrentWeatherCard({ weather }) {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Current Weather
        </Typography>

        <Stack spacing={1}>
          <Typography>Temperature: {weather.temperature}</Typography>
          <Typography>Humidity: {weather.humidity}</Typography>
          <Typography>Condition: {weather.condition}</Typography>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default CurrentWeatherCard;