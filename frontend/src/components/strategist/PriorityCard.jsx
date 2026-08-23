import { Card, CardContent, Typography, Chip, Stack } from "@mui/material";

function PriorityCard({ item }) {
  if (!item) return null;

  const getColor = (level) => {
    if (level === "High") return "error";
    if (level === "Medium") return "warning";
    return "success";
  };

  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Stack spacing={1.5}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            {item.title}
          </Typography>

          <Chip
            label={`${item.level} Priority`}
            color={getColor(item.level)}
            sx={{ width: "fit-content", fontWeight: 600 }}
          />

          <Typography variant="body2" color="text.secondary">
            {item.description}
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default PriorityCard;