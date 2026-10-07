import { Box, Typography, Paper } from "@mui/material";

function EmptyState({ title, description, action }) {
  return (
    <Paper 
      elevation={0}
      sx={{ 
        p: 6, 
        textAlign: "center", 
        border: "1px dashed",
        borderColor: "divider",
        backgroundColor: "background.default",
        borderRadius: 4,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: 250
      }}
    >

      <Typography variant="h6" fontWeight={700} color="text.primary" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: action ? 3 : 0, maxWidth: 500 }}>
        {description}
      </Typography>
      {action && <Box>{action}</Box>}
    </Paper>
  );
}

export default EmptyState;
