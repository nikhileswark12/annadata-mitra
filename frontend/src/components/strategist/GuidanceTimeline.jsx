import {
  Card,
  CardContent,
  Typography,
  Stack,
  Box,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";

function GuidanceTimeline({ timeline }) {
  if (!timeline || timeline.length === 0) return null;

  return (
    <Card elevation={3} sx={{ borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Action Timeline
        </Typography>

        <Stack spacing={3} sx={{ mt: 2 }}>
          {timeline.map((block, index) => (
            <Box
              key={index}
              sx={{
                borderLeft: "4px solid #2e7d32",
                pl: 2,
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                {block.phase}
              </Typography>

              <List sx={{ p: 0 }}>
                {block.actions.map((action, actionIndex) => (
                  <ListItem key={actionIndex} sx={{ px: 0, py: 0.5 }}>
                    <ListItemText primary={action} />
                  </ListItem>
                ))}
              </List>
            </Box>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}

export default GuidanceTimeline;