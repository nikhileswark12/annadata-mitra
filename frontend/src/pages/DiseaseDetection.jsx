import { useState, useRef } from "react";
import Grid from "@mui/material/Grid";
import {
  Box,
  Button,
  Paper,
  Stack,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from "@mui/material";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import ImageSearchIcon from "@mui/icons-material/ImageSearch";

import Layout from "../components/common/Layout";
import PageHeader from "../components/common/PageHeader";
import { analyzeCropImage } from "../services/visionService";
import AIResultCard from "../components/common/AIResultCard";
import EmptyState from "../components/common/EmptyState";
import { ResultLoadingState } from "../components/common/Loader";
import ErrorState from "../components/common/ErrorState";

function DiseaseDetection() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileError, setFileError] = useState("");
  const fileInputRef = useRef(null);

  const handleImageChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
      setFileError("Invalid file type. Please select a JPG, JPEG, or PNG image.");
      return;
    }

    setFileError("");
    setError(null);
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("image", selectedImage);

      const response = await analyzeCropImage(formData);

      if (response.data?.success === true) {
        setResult(response.data.data);
      } else {
        setError({
            message: "Failed to analyze image",
            details: "The vision service returned an unsuccessful response. Please try again."
        });
      }
    } catch (err) {
      console.error(err);
      setError({
        message: "Analysis Failed",
        details: err.response?.data?.message || err.message || "Failed to connect to the vision service. Please try again."
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setPreviewUrl("");
    setResult(null);
    setError(null);
    setFileError("");
    if (fileInputRef.current) {
        fileInputRef.current.value = '';
    }
  };

  const renderTreatments = (treatmentString) => {
    if (!treatmentString) return null;
    const treatments = treatmentString.split('\n').filter(t => t.trim() !== '');
    if (treatments.length === 0) return null;
    
    return (
      <Paper
        variant="outlined"
        sx={{
          p: 3,
          borderRadius: 3,
          backgroundColor: "#f8fff8",
          borderColor: "#c8e6c9",
          mt: 2
        }}
      >
        <Typography variant="subtitle1" fontWeight={700} mb={1}>
          Recommended Actions
        </Typography>
        <List dense disablePadding>
          {treatments.map((item, index) => (
            <ListItem key={index} disableGutters sx={{ alignItems: "flex-start", py: 0.5 }}>
              <ListItemIcon sx={{ minWidth: 28, mt: 0.5 }}>
                <CheckCircleOutlineIcon color="success" fontSize="small" />
              </ListItemIcon>
              <ListItemText 
                primary={item.replace(/^\d+\.\s*/, '').trim()}
                primaryTypographyProps={{ variant: "body2", color: "text.primary", fontWeight: 500 }}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    );
  };

  return (
    <Layout>
      <PageHeader
        title="Disease Detection"
        subtitle="Upload a crop image to identify disease symptoms and get actionable treatment advice."
      />

      <Grid container spacing={4}>
        <Grid item xs={12} md={5}>
          <Stack spacing={4}>
            <Paper elevation={0} variant="outlined" sx={{ p: 4, borderRadius: 4, borderColor: "divider" }}>
              <Stack spacing={3}>
                <Box>
                  <Typography variant="h6" fontWeight={700} gutterBottom>
                    Analyze Crop Image
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Select a clear, well-lit photo of the affected plant leaf or crop area.
                  </Typography>
                </Box>

                <Paper
                  variant="outlined"
                  sx={{
                    p: 4,
                    borderRadius: 4,
                    textAlign: "center",
                    borderStyle: "dashed",
                    borderColor: selectedImage ? "#2e7d32" : "divider",
                    backgroundColor: selectedImage ? "#f8fff8" : "transparent",
                    transition: "all 0.2s ease"
                  }}
                >
                  <Stack spacing={2} alignItems="center">
                    {previewUrl ? (
                      <Box sx={{ position: 'relative', width: '100%', mb: 2 }}>
                        <Box
                          component="img"
                          src={previewUrl}
                          alt="Selected crop preview"
                          sx={{
                            width: "100%",
                            height: 240,
                            objectFit: "contain",
                            borderRadius: 2,
                            bgcolor: 'rgba(0,0,0,0.02)'
                          }}
                        />
                        <Button
                          size="small"
                          color="error"
                          onClick={handleClear}
                          disabled={loading}
                          sx={{ mt: 1, textTransform: "none", fontWeight: 600 }}
                        >
                          Remove Image
                        </Button>
                      </Box>
                    ) : (
                      <Box sx={{ py: 3, textAlign: "center" }}>
                        <CloudUploadIcon sx={{ fontSize: 48, color: "text.secondary", mb: 1 }} />
                        <Typography variant="subtitle1" fontWeight={600} gutterBottom>
                          Upload Image
                        </Typography>
                        <Typography variant="body2" color="text.secondary" mb={3}>
                          Supported formats: JPG, JPEG, PNG
                        </Typography>
                      </Box>
                    )}

                    <Button
                      variant={previewUrl ? "outlined" : "contained"}
                      component="label"
                      disabled={loading}
                      fullWidth
                      sx={{
                        borderRadius: 2,
                        textTransform: "none",
                        fontWeight: 600,
                        py: 1
                      }}
                    >
                      {previewUrl ? "Change Image" : "Choose Image"}
                      <input 
                        type="file" 
                        hidden 
                        accept="image/jpeg, image/png, image/jpg" 
                        onChange={handleImageChange}
                        ref={fileInputRef}
                      />
                    </Button>
                    
                    {fileError && (
                      <Typography variant="caption" color="error.main" sx={{ mt: 1, display: 'block' }}>
                        {fileError}
                      </Typography>
                    )}
                  </Stack>
                </Paper>

                <Button
                  variant="contained"
                  startIcon={<ImageSearchIcon />}
                  onClick={handleAnalyze}
                  disabled={!selectedImage || loading}
                  fullWidth
                  sx={{
                    py: 1.5,
                    borderRadius: 2,
                    textTransform: "none",
                    fontWeight: 700,
                    backgroundColor: "#2e7d32",
                  }}
                >
                  {loading ? "Analyzing Image..." : "Analyze Image"}
                </Button>
              </Stack>
            </Paper>

            <Paper elevation={0} variant="outlined" sx={{ p: 3, borderRadius: 4, borderColor: "divider", backgroundColor: "rgba(0,0,0,0.01)" }}>
              <Typography variant="subtitle2" fontWeight={700} gutterBottom>
                Image Guidelines
              </Typography>
              <List dense disablePadding sx={{ '& .MuiListItem-root': { px: 0 } }}>
                <ListItem><ListItemText primary="• Ensure the affected area is in focus" primaryTypographyProps={{ variant: "body2", color: "text.secondary" }} /></ListItem>
                <ListItem><ListItemText primary="• Avoid blurry or dark photos" primaryTypographyProps={{ variant: "body2", color: "text.secondary" }} /></ListItem>
                <ListItem><ListItemText primary="• One leaf/plant per image works best" primaryTypographyProps={{ variant: "body2", color: "text.secondary" }} /></ListItem>
              </List>
            </Paper>
          </Stack>
        </Grid>

        <Grid item xs={12} md={7}>
          <Stack spacing={3} sx={{ height: "100%" }}>
            {loading ? (
              <ResultLoadingState 
                height="100%" 
                minHeight={400} 
                message="Analyzing crop image..."
              />
            ) : error ? (
              <Box sx={{ pt: 2 }}>
                <ErrorState 
                  title={error.message}
                  message={error.details}
                  onRetry={handleAnalyze}
                />
              </Box>
            ) : result ? (
              <AIResultCard
                title="Analysis Complete"
                primaryResult={result.disease}
                confidence={result.confidence}
                severity={result.severity}
                explanation={result.description}
              >
                {renderTreatments(result.treatment)}
              </AIResultCard>
            ) : (
              <Box sx={{ pt: 2, height: "100%" }}>
                <EmptyState 
                  title="No Analysis Result" 
                  description="Select an image and click 'Analyze Image' to identify diseases and receive actionable treatment recommendations."
                />
              </Box>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default DiseaseDetection;