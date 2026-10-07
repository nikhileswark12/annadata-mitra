import { Box, Typography, Stack } from "@mui/material";

function PageHeader({ title, subtitle, action }) {
  return (
    <Box sx={{ mb: 4, display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 2 }}>
      <Stack spacing={1}>
        <Box>
          <Typography variant="h4" color="primary.main" fontWeight={800}>
            {title}
          </Typography>
        </Box>
        {subtitle && (
          <Typography variant="body1" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </Stack>
      {action && <Box>{action}</Box>}
    </Box>
  );
}

export default PageHeader;