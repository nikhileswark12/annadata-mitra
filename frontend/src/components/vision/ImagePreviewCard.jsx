import { Card, CardContent, Typography, Box } from "@mui/material";

function ImagePreviewCard({ imagePreview }) {
  return (
    <Card elevation={2} sx={{ minHeight: 320 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Image Preview
        </Typography>

        {imagePreview ? (
          <Box
            component="img"
            src={imagePreview}
            alt="Crop preview"
            sx={{
              width: "100%",
              maxHeight: 250,
              objectFit: "cover",
              borderRadius: 2,
            }}
          />
        ) : (
          <Box
            sx={{
              height: 250,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: "2px dashed #c8e6c9",
              borderRadius: 2,
              backgroundColor: "#f8fff8",
              color: "#666",
              textAlign: "center",
              px: 2,
            }}
          >
            <Typography variant="body1">
              No image selected yet. Upload a crop image to preview it here.
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default ImagePreviewCard;