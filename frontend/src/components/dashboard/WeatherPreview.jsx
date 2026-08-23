import { Card, CardContent, Typography, Stack } from "@mui/material";

function WeatherPreview() {
  const previewData = [
    { label: "Temperature", value: "31°C" },
    { label: "Humidity", value: "68%" },
    { label: "Condition", value: "Partly Cloudy" },
  ];

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Weather Preview
        </Typography>

        <Stack spacing={1}>
          {previewData.map((item) => (
            <Typography key={item.label}>
              <strong>{item.label}:</strong> {item.value}
            </Typography>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}

export default WeatherPreview;