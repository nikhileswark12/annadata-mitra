import {
  Card,
  CardContent,
  Typography,
  Chip,
  Stack,
  Box,
} from "@mui/material";
import WarningAmberRoundedIcon from "@mui/icons-material/WarningAmberRounded";
import CheckCircleRoundedIcon from "@mui/icons-material/CheckCircleRounded";
import BiotechRoundedIcon from "@mui/icons-material/BiotechRounded";

function DiseaseResultCard({ result }) {
  if (!result) return null;

  const getSeverityColor = (severity) => {
    if (severity === "High") return "error";
    if (severity === "Medium") return "warning";
    return "success";
  };

  const isHealthy =
    result.status?.toLowerCase() === "healthy" ||
    result.disease?.toLowerCase() === "healthy";

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Analysis Result
        </Typography>

        <Stack spacing={2.2}>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1.2,
              p: 1.5,
              borderRadius: 2,
              backgroundColor: isHealthy ? "#e8f5e9" : "#fff8e1",
            }}
          >
            {isHealthy ? (
              <CheckCircleRoundedIcon color="success" />
            ) : (
              <WarningAmberRoundedIcon color="warning" />
            )}
            <Typography variant="body1" sx={{ fontWeight: 600 }}>
              {result.status}
            </Typography>
          </Box>

          <Box>
            <Typography variant="body2" color="text.secondary">
              Detected condition
            </Typography>
            <Typography variant="h6" sx={{ fontWeight: 700 }}>
              {result.disease}
            </Typography>
          </Box>

          <Box>
            <Typography variant="body2" color="text.secondary">
              Confidence score
            </Typography>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <BiotechRoundedIcon color="primary" fontSize="small" />
              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                {result.confidence}%
              </Typography>
            </Box>
          </Box>

          <Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              Severity
            </Typography>
            <Chip
              label={result.severity}
              color={getSeverityColor(result.severity)}
              sx={{ fontWeight: 600 }}
            />
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default DiseaseResultCard;