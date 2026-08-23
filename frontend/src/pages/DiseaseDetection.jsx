import { useState } from "react";
import Grid from "@mui/material/Grid";
import {
  Alert,
  Box,
  Button,
  Chip,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import ImageSearchIcon from "@mui/icons-material/ImageSearch";
import { analyzeCropImage } from "../services/visionService";

function DiseaseDetection() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleImageChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
      setError("Invalid file type. Please select a JPG, JPEG, or PNG image.");
      setSelectedImage(null);
      setPreviewUrl("");
      return;
    }

    setError("");
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setMessage("Image selected successfully. Ready for analysis.");
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setMessage("Please upload an image before analysis.");
      return;
    }

    setLoading(true);
    setMessage("");
    setError("");

    try {
      const formData = new FormData();
      formData.append("image", selectedImage);

      const response = await analyzeCropImage(formData);

      if (response.data?.success === true) {
        setResult(response.data.data);
        setMessage("Disease analysis completed successfully.");
      } else {
        setError("Failed to analyze image.");
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    if (severity === "High") return "error";
    if (severity === "Medium") return "warning";
    if (severity === "Low") return "success";
    return "default";
  };

  return (
    <Layout>
      <PageHeader
        title="Disease Detection"
        subtitle="Upload a crop image to identify disease symptoms and get treatment recommendations."
      />

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Box>
                <Typography variant="h5" fontWeight={800} gutterBottom>
                  Upload Crop Image
                </Typography>
                <Typography color="text.secondary">
                  Add a clear leaf or crop photo to detect disease symptoms and get treatment suggestions.
                </Typography>
              </Box>

              <Paper
                variant="outlined"
                sx={{
                  p: 4,
                  borderRadius: 4,
                  textAlign: "center",
                  borderStyle: "dashed",
                  borderColor: "#a5d6a7",
                  backgroundColor: "#f8fff8",
                }}
              >
                <Stack spacing={2} alignItems="center">
                  <CloudUploadIcon sx={{ fontSize: 52, color: "#2e7d32" }} />

                  <Typography variant="h6">
                    Choose an image from your device
                  </Typography>

                  <Typography variant="body2" color="text.secondary">
                    Supported formats: JPG, PNG, JPEG
                  </Typography>

                  <Button
                    variant="outlined"
                    component="label"
                    sx={{
                      borderRadius: 3,
                      textTransform: "none",
                      fontWeight: 700,
                    }}
                  >
                    Choose Image
                    <input type="file" hidden accept="image/*" onChange={handleImageChange} />
                  </Button>
                </Stack>
              </Paper>

              <Button
                variant="contained"
                startIcon={<ImageSearchIcon />}
                onClick={handleAnalyze}
                disabled={!selectedImage || loading}
                sx={{
                  py: 1.4,
                  borderRadius: 3,
                  textTransform: "none",
                  fontWeight: 700,
                  backgroundColor: "#2e7d32",
                }}
              >
                {loading ? "Analyzing..." : "Analyze Image"}
              </Button>

              {error && (
                <Alert severity="error" sx={{ borderRadius: 3 }}>
                  {error}
                </Alert>
              )}

              {message && !error && (
                <Alert severity={result ? "success" : "info"} sx={{ borderRadius: 3 }}>
                  {message}
                </Alert>
              )}
            </Stack>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Typography variant="h5" fontWeight={800}>
                Image Preview
              </Typography>

              <Paper
                variant="outlined"
                sx={{
                  minHeight: 320,
                  borderRadius: 4,
                  borderStyle: "dashed",
                  borderColor: "#c8e6c9",
                  backgroundColor: "#f8fff8",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  overflow: "hidden",
                  p: 2,
                }}
              >
                {previewUrl ? (
                  <Box
                    component="img"
                    src={previewUrl}
                    alt="Crop preview"
                    sx={{
                      maxWidth: "100%",
                      maxHeight: 300,
                      objectFit: "contain",
                      borderRadius: 3,
                    }}
                  />
                ) : (
                  <Typography color="text.secondary">
                    No image selected yet. Upload a crop image to preview it here.
                  </Typography>
                )}
              </Paper>
            </Stack>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Paper elevation={3} sx={{ p: 3, borderRadius: 4, height: "100%" }}>
            <Stack spacing={2}>
              <Typography variant="h6" fontWeight={800}>
                Detection Benefits
              </Typography>

              {[
                "Early disease detection can reduce crop loss.",
                "Clear leaf images improve accuracy of prediction.",
                "Treatment guidance helps farmers act quickly.",
              ].map((item, index) => (
                <Paper
                  key={index}
                  variant="outlined"
                  sx={{
                    p: 2,
                    borderRadius: 3,
                    borderColor: "#dcedc8",
                    backgroundColor: "#fcfff9",
                  }}
                >
                  <Box display="flex" alignItems="flex-start" gap={1}>
                    <CheckCircleOutlineIcon fontSize="small" sx={{ mt: 0.5 }} />
                    <Typography variant="body2">{item}</Typography>
                  </Box>
                </Paper>
              ))}
            </Stack>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Paper elevation={3} sx={{ p: 4, borderRadius: 4, height: "100%" }}>
            <Stack spacing={3}>
              <Typography variant="h5" fontWeight={800}>
                Detection Result
              </Typography>

              {result ? (
                <>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label={`Disease: ${result.disease}`} color="success" />
                    <Chip label={`Confidence: ${result.confidence}%`} variant="outlined" />
                    <Chip label={`Severity: ${result.severity}`} color={getSeverityColor(result.severity)} />
                  </Stack>

                  <Typography variant="body2" fontStyle="italic" color="text.secondary" mt={2}>
                    {result.description}
                  </Typography>

                  <Grid container spacing={2} mt={1}>
                    <Grid size={{ xs: 12 }}>
                      <Paper
                        variant="outlined"
                        sx={{
                          p: 3,
                          borderRadius: 3,
                          backgroundColor: "#f8fff8",
                          borderColor: "#c8e6c9",
                          height: "100%",
                        }}
                      >
                        <Typography variant="h6" fontWeight={700} mb={2}>
                          Treatment Suggestions
                        </Typography>
                        <Stack spacing={1}>
                          {result.treatment?.split('\n').filter(t => t.trim() !== '').map((item, index) => (
                            <Box key={index} display="flex" gap={1} alignItems="flex-start">
                              <CheckCircleOutlineIcon fontSize="small" sx={{ mt: 0.6 }} />
                              <Typography variant="body2">{item.trim()}</Typography>
                            </Box>
                          ))}
                        </Stack>
                      </Paper>
                    </Grid>
                  </Grid>
                </>
              ) : (
                <Typography color="text.secondary">
                  Upload and analyze an image to see detected disease information, confidence score, treatment advice, and prevention tips.
                </Typography>
              )}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default DiseaseDetection;