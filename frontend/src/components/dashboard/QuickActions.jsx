import { Card, CardContent, Typography, Button, Stack } from "@mui/material";
import { Link } from "react-router-dom";

function QuickActions() {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Quick Actions
        </Typography>

        <Stack direction="row" spacing={2} flexWrap="wrap">
          <Button component={Link} to="/crop-planning" variant="contained">
            Open Crop Planning
          </Button>
          <Button component={Link} to="/weather-risk" variant="outlined">
            Open Weather Risk
          </Button>
          <Button component={Link} to="/login" variant="text">
            Farmer Login
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default QuickActions;