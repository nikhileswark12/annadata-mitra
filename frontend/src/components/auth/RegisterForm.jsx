import { useState } from "react";
import { TextField, Button, Paper, Typography, Stack, Alert } from "@mui/material";
import { registerUser } from "../../services/authService";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

function RegisterForm() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: "",
    mobileNumber: "",
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
    console.log("REGISTER SUBMIT HIT:", formData);

    setLoading(true);
    setSuccessMessage("");
    setErrorMessage("");

    try {
      const response = await registerUser(formData);
      console.log("REGISTER SUCCESS:", response);

      if (response.success === true) {
        const token = response.data.token;
        const user = response.data.user;
        login(token, user);
      }

      setSuccessMessage(response.message || "Registration successful.");
    } catch (error) {
      console.error("REGISTER ERROR:", error);
      
      let errorMsg = error.message || "Registration failed. Please try again.";
      if (error.details && error.details.length > 0) {
        errorMsg = error.details[0].message;
      }

      setErrorMessage(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 450, mx: "auto", mt: 4, borderRadius: 3 }}>
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Register
      </Typography>

      <form onSubmit={handleSubmit}>
        <Stack spacing={2}>
          {successMessage && <Alert severity="success">{successMessage}</Alert>}
          {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

          <TextField
            label="Full Name"
            name="fullName"
            value={formData.fullName}
            onChange={handleChange}
            fullWidth
            required
          />

          <TextField
            label="Mobile Number"
            name="mobileNumber"
            value={formData.mobileNumber}
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
            {loading ? "Registering..." : "Register"}
          </Button>
        </Stack>
      </form>
    </Paper>
  );
}

export default RegisterForm;