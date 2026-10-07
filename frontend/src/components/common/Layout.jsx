import { Container, Box, Typography } from "@mui/material";

function Layout({ title, children }) {
  return (
    <Container maxWidth="lg" sx={{ py: 4, minHeight: "100vh" }}>
      {title && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h4" color="primary" gutterBottom>
            {title}
          </Typography>
        </Box>
      )}
      <Box>{children}</Box>
    </Container>
  );
}

export default Layout;