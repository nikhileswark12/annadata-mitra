import { Card, CardContent, Alert, Stack, Typography } from "@mui/material";

function RiskAlertList({ alerts }) {
  const mapSeverity = (severity) => {
    if (severity === "HIGH") return "error";
    if (severity === "MEDIUM") return "warning";
    return "info";
  };

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Risk Alerts
        </Typography>

        <Stack spacing={2}>
          {alerts.map((alert, index) => (
            <Alert severity={mapSeverity(alert.severity)} key={index}>
              {alert.severity}: {alert.message}
            </Alert>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}

export default RiskAlertList;