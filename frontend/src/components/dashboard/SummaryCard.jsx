import { Card, CardContent, Typography } from "@mui/material";

function SummaryCard({ title, value, subtitle }) {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h4" color="primary">
          {value}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {subtitle}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default SummaryCard;