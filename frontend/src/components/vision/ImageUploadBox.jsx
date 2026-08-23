import { Card, CardContent, Typography, Button, Stack, Box } from "@mui/material";
import CloudUploadOutlinedIcon from "@mui/icons-material/CloudUploadOutlined";
import ImageSearchOutlinedIcon from "@mui/icons-material/ImageSearchOutlined";

function ImageUploadBox({ onFileChange, onAnalyze, loading, selectedFile }) {
  return (
    <Card elevation={3} sx={{ borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Upload Crop Image
        </Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Add a clear leaf or crop photo to detect disease symptoms and get treatment suggestions.
        </Typography>

        <Box
          sx={{
            border: "2px dashed #a5d6a7",
            borderRadius: 3,
            backgroundColor: "#f8fff8",
            p: 3,
            textAlign: "center",
            mb: 2,
          }}
        >
          <CloudUploadOutlinedIcon sx={{ fontSize: 42, color: "#2e7d32", mb: 1 }} />

          <Typography variant="body1" sx={{ fontWeight: 500, mb: 1 }}>
            Choose an image from your device
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Supported formats: JPG, PNG, JPEG
          </Typography>

          <Button variant="outlined" component="label">
            Choose Image
            <input type="file" hidden accept="image/*" onChange={onFileChange} />
          </Button>
        </Box>

        {selectedFile && (
          <Box
            sx={{
              backgroundColor: "#f1f8e9",
              borderRadius: 2,
              p: 1.5,
              mb: 2,
            }}
          >
            <Typography variant="body2" color="text.secondary">
              Selected file:
            </Typography>
            <Typography variant="body1" sx={{ fontWeight: 500 }}>
              {selectedFile.name}
            </Typography>
          </Box>
        )}

        <Stack spacing={2}>
          <Button
            variant="contained"
            startIcon={<ImageSearchOutlinedIcon />}
            onClick={onAnalyze}
            disabled={!selectedFile || loading}
            sx={{ py: 1.2 }}
          >
            {loading ? "Analyzing..." : "Analyze Image"}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default ImageUploadBox;