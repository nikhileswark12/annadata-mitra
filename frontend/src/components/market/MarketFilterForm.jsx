import { Card, CardContent, TextField, Button, Stack, Typography } from "@mui/material";
import Grid from "@mui/material/Grid";

function MarketFilterForm({ formData, onChange, onSubmit, onReset, loading }) {
  return (
    <Card elevation={3} sx={{ borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Market Filters
        </Typography>

        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Crop Name"
              name="crop"
              value={formData.crop}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Quantity (kg)"
              name="quantity"
              type="number"
              value={formData.quantity}
              onChange={onChange}
              inputProps={{ min: 0 }}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Location"
              name="location"
              value={formData.location}
              onChange={onChange}
            />
          </Grid>

          <Grid size={12}>
            <Stack direction="row" spacing={2}>
              <Button variant="contained" onClick={onSubmit} disabled={loading}>
                {loading ? "Loading..." : "Get Market Insights"}
              </Button>
              <Button variant="outlined" onClick={onReset}>
                Reset
              </Button>
            </Stack>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

export default MarketFilterForm;