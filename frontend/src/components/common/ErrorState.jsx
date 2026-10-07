import { Box, Typography, Button, Paper } from "@mui/material";


function ErrorState({ message, onRetry }) {
  return (
    <Paper 
      elevation={0}
      sx={{ 
        p: 4, 
        textAlign: "center", 
        border: "1px solid",
        borderColor: "error.light",
        backgroundColor: "error.lighter",
        borderRadius: 3 
      }}
    >

      <Typography variant="h6" color="error.main" gutterBottom>
        Something went wrong
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3, maxWidth: 500, mx: "auto" }}>
        {message || "We encountered an unexpected error while trying to load this data. Please try again."}
      </Typography>
      {onRetry && (
        <Button 
          variant="outlined" 
          color="error" 
          onClick={onRetry}
          sx={{ fontWeight: 600 }}
        >
          Try Again
        </Button>
      )}
    </Paper>
  );
}

export default ErrorState;
