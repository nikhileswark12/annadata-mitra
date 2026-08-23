import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#2E7D32",
    },
    secondary: {
      main: "#1565C0",
    },
    success: {
      main: "#388E3C",
    },
    warning: {
      main: "#F9A825",
    },
    error: {
      main: "#D32F2F",
    },
    background: {
      default: "#F4F7F4",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#1F2937",
      secondary: "#4B5563",
    },
  },
  typography: {
    fontFamily: "Arial, sans-serif",
    h4: {
      fontWeight: 700,
    },
    h5: {
      fontWeight: 600,
    },
    button: {
      textTransform: "none",
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
});

export default theme;