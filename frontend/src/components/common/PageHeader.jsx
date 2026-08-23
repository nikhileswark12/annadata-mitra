import { Box, Typography } from "@mui/material";

function PageHeader({ title, subtitle }) {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h4" color="primary" gutterBottom>
        {title}
      </Typography>
      {subtitle && (
        <Typography variant="body1" color="text.secondary">
          {subtitle}
        </Typography>
      )}
    </Box>
  );
}

export default PageHeader;