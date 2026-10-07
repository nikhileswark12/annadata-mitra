import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#2E7D32", // Green 800
      light: "#4CAF50",
      dark: "#1B5E20",
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#1565C0", // Blue 800
      light: "#42A5F5",
      dark: "#0D47A1",
      contrastText: "#FFFFFF",
    },
    success: {
      main: "#2E7D32",
      light: "#E8F5E9",
      dark: "#1B5E20",
    },
    warning: {
      main: "#ED6C02",
      light: "#FFF3E0",
      dark: "#E65100",
    },
    error: {
      main: "#D32F2F",
      light: "#FFEBEE",
      dark: "#C62828",
    },
    info: {
      main: "#0288D1",
      light: "#E1F5FE",
      dark: "#01579B",
    },
    background: {
      default: "#F4F7F4", // Soft green-gray
      paper: "#FFFFFF",
    },
    text: {
      primary: "#1F2937", // Gray 800
      secondary: "#4B5563", // Gray 600
      disabled: "#9CA3AF", // Gray 400
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontSize: "2.5rem", fontWeight: 700, lineHeight: 1.2 },
    h2: { fontSize: "2rem", fontWeight: 700, lineHeight: 1.3 },
    h3: { fontSize: "1.75rem", fontWeight: 700, lineHeight: 1.3 },
    h4: { fontSize: "1.5rem", fontWeight: 700, lineHeight: 1.4 },
    h5: { fontSize: "1.25rem", fontWeight: 700, lineHeight: 1.4 },
    h6: { fontSize: "1rem", fontWeight: 700, lineHeight: 1.5 },
    subtitle1: { fontSize: "1rem", fontWeight: 600, lineHeight: 1.5 },
    subtitle2: { fontSize: "0.875rem", fontWeight: 600, lineHeight: 1.57 },
    body1: { fontSize: "1rem", fontWeight: 400, lineHeight: 1.5 },
    body2: { fontSize: "0.875rem", fontWeight: 400, lineHeight: 1.43 },
    button: { textTransform: "none", fontWeight: 600 },
    caption: { fontSize: "0.75rem", fontWeight: 400, lineHeight: 1.66 },
    overline: { fontSize: "0.75rem", fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase" },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: "8px 24px",
          boxShadow: "none",
          "&:hover": {
            boxShadow: "none",
          },
        },
        containedPrimary: {
          "&:hover": {
            backgroundColor: "#1B5E20",
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
        elevation1: {
          boxShadow: "0px 1px 3px rgba(0, 0, 0, 0.05), 0px 1px 2px rgba(0, 0, 0, 0.1)",
        },
        elevation2: {
          boxShadow: "0px 4px 6px -1px rgba(0, 0, 0, 0.1), 0px 2px 4px -1px rgba(0, 0, 0, 0.06)",
        },
        elevation3: {
          boxShadow: "0px 10px 15px -3px rgba(0, 0, 0, 0.1), 0px 4px 6px -2px rgba(0, 0, 0, 0.05)",
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: "0px 4px 6px -1px rgba(0, 0, 0, 0.1), 0px 2px 4px -1px rgba(0, 0, 0, 0.06)",
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 8,
          },
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

export default theme;