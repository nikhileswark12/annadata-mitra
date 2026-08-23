import { Card, CardContent, Typography, Box } from "@mui/material";

function ConflictResolutionCard({ conflictResolution }) {
  if (!conflictResolution) return null;

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Conflict Resolution
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Issue
          </Typography>
          <Typography variant="body1" sx={{ fontWeight: 500 }}>
            {conflictResolution.issue}
          </Typography>
        </Box>

        <Box>
          <Typography variant="body2" color="text.secondary">
            Recommended Resolution
          </Typography>
          <Typography variant="body1" sx={{ fontWeight: 500 }}>
            {conflictResolution.resolution}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

export default ConflictResolutionCard;