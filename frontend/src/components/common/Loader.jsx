import { Box, CircularProgress, Skeleton, Stack, Typography } from "@mui/material";

export function LoadingState({ message = "Loading..." }) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100%', minHeight: 200, gap: 2 }}>
      <CircularProgress color="primary" />
      <Typography color="text.secondary">{message}</Typography>
    </Box>
  );
}

export function PageLoadingState() {
  return (
    <Stack spacing={3} sx={{ mt: 4 }}>
      <Skeleton variant="text" width="40%" height={60} />
      <Skeleton variant="text" width="60%" height={30} />
      <Box sx={{ display: "flex", gap: 3, flexWrap: "wrap", mt: 4 }}>
        <Skeleton variant="rectangular" width={250} height={150} sx={{ borderRadius: 2 }} />
        <Skeleton variant="rectangular" width={250} height={150} sx={{ borderRadius: 2 }} />
        <Skeleton variant="rectangular" width={250} height={150} sx={{ borderRadius: 2 }} />
      </Box>
    </Stack>
  );
}

export function ResultLoadingState({ lines = 3, height = 300 }) {
  return (
    <Box sx={{ p: 3, border: "1px solid", borderColor: "divider", borderRadius: 3, height }}>
      <Stack spacing={2}>
        <Skeleton variant="text" width="30%" height={40} />
        {Array.from({ length: lines }).map((_, i) => (
          <Skeleton key={i} variant="text" width={`${90 - (i * 10)}%`} height={24} />
        ))}
      </Stack>
    </Box>
  );
}

export default LoadingState;