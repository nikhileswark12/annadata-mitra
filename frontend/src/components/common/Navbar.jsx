import { Link, useLocation, useNavigate } from "react-router-dom";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { useAuth } from "../../context/AuthContext";

function Navbar() {
  const location = useLocation();
  const { logout } = useAuth();
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const navLinks = [
    { label: "Dashboard", path: "/" },
    { label: "Crop Planning", path: "/crop-planning" },
    { label: "Weather Risk", path: "/weather-risk" },
    { label: "Disease Detection", path: "/disease-detection" },
    { label: "Market Intelligence", path: "/market-intelligence" },
    { label: "Strategist", path: "/strategist" },
  ];

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: "#f3f7f1",
        color: "#1b5e20",
        boxShadow: 1,
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 2,
        }}
      >
        <Typography
          variant="h4"
          component={Link}
          to="/"
          sx={{
            textDecoration: "none",
            color: "#1b5e20",
            fontWeight: 800,
          }}
        >
          Annadata Mitra
        </Typography>

        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, alignItems: "center" }}>
          {user && navLinks.map((item) => (
            <Button
              key={item.path}
              component={Link}
              to={item.path}
              variant={location.pathname === item.path ? "contained" : "text"}
              sx={{
                fontWeight: 700,
                borderRadius: 2,
                textTransform: "none",
              }}
            >
              {item.label}
            </Button>
          ))}

          {user ? (
            <>
              <Typography
                sx={{
                  ml: 1,
                  fontWeight: 700,
                  color: "#1b5e20",
                }}
              >
                Hi, {user.fullName}
              </Typography>

              <Button
                variant="outlined"
                color="success"
                onClick={logout}
                sx={{
                  fontWeight: 700,
                  borderRadius: 2,
                  textTransform: "none",
                }}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button
                component={Link}
                to="/login"
                variant={location.pathname === "/login" ? "contained" : "text"}
                sx={{
                  fontWeight: 700,
                  borderRadius: 2,
                  textTransform: "none",
                }}
              >
                Login
              </Button>

              <Button
                component={Link}
                to="/register"
                variant={location.pathname === "/register" ? "contained" : "text"}
                sx={{
                  fontWeight: 700,
                  borderRadius: 2,
                  textTransform: "none",
                }}
              >
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;