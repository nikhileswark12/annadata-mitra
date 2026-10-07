import { Paper, Stack, Typography, Box } from "@mui/material";

function MetricCard({ title, value, subtitle, color = "primary" }) {
  return (
    <Paper elevation={3} sx={{ p: 3, height: "100%", display: "flex", flexDirection: "column" }}>
      <Stack spacing={1} sx={{ flexGrow: 1 }}>
        <Box>
          <Typography variant="subtitle1" fontWeight={700} sx={{ color: `${color}.main` }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" fontWeight={800}>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </Stack>
    </Paper>
  );
}

export default MetricCard;
