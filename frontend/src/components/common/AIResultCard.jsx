import { Paper, Stack, Typography, Box, Chip } from "@mui/material";

import StatusChip from "./StatusChip";

function AIResultCard({ 
  title, 
  primaryResult, 
  confidence, 
  severity, 
  explanation, 
  children 
}) {
  return (
    <Paper elevation={3} sx={{ p: 4, borderRadius: 4, borderTop: "4px solid", borderColor: "primary.main" }}>
      <Stack spacing={3}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" flexWrap="wrap" gap={2}>
          <Box>
            <Typography variant="h6" fontWeight={800} color="primary.main">
              {title}
            </Typography>
          </Box>
          <Box display="flex" gap={1} flexWrap="wrap">
            {confidence && (
              <Chip 
                label={`${confidence}% Confidence`} 
                size="small" 
                color={confidence > 80 ? "success" : "warning"}
                variant="outlined" 
                sx={{ fontWeight: 700 }}
              />
            )}
            {severity && (
              <StatusChip status={severity} size="small" />
            )}
          </Box>
        </Box>

        <Typography variant="h4" fontWeight={800} color="text.primary">
          {primaryResult}
        </Typography>

        {explanation && (
          <Typography variant="body1" color="text.secondary" sx={{ fontStyle: "italic", bgcolor: "background.default", p: 2, borderRadius: 2 }}>
            {explanation}
          </Typography>
        )}

        {children && (
          <Box mt={1}>
            {children}
          </Box>
        )}
      </Stack>
    </Paper>
  );
}

export default AIResultCard;
