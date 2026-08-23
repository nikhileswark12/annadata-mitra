import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Paper, Typography, Stack, Alert } from "@mui/material";
import { loginUser } from "../../services/authService";
import { useAuth } from "../../context/AuthContext";

function LoginForm() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    identifier: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage("");
    setErrorMessage("");

    try {
      const response = await loginUser(formData);

      if (response.success === true) {
        const token = response.data.token;
        const user = response.data.user;
        login(token, user);
      }

      setSuccessMessage(response.message || "Login successful.");

      // Optional delay since login handles redirect, but we might want to let the context do it.
      // The context login function handles redirection, but wait, login doesn't await. 
      // AuthContext's login does redirect syncly, we don't need navigate here anymore, but keeping it doesn't hurt if we remove navigate from it.
      // Wait, AuthContext handles navigate.
    } catch (error) {
      console.error("Login error:", error);
      setErrorMessage(
        error.message || "Login failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 450, mx: "auto", mt: 4, borderRadius: 3 }}>
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Login
      </Typography>

      <form onSubmit={handleSubmit}>
        <Stack spacing={2}>
          {successMessage && <Alert severity="success">{successMessage}</Alert>}
          {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

          <TextField
            label="Email or Mobile"
            name="identifier"
            value={formData.identifier}
            onChange={handleChange}
            fullWidth
            required
          />

          <TextField
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            fullWidth
            required
          />

          <Button type="submit" variant="contained" size="large" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </Button>
        </Stack>
      </form>
    </Paper>
  );
}

export default LoginForm;