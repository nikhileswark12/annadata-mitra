import { Card, CardContent, TextField, Button, Stack } from "@mui/material";
import Grid from "@mui/material/Grid";

function SoilInputForm({ formData, onChange, onSubmit, onReset, loading }) {
  return (
    <Card elevation={2}>
      <CardContent>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Nitrogen (N)"
              name="nitrogen"
              type="number"
              value={formData.nitrogen}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Phosphorus (P)"
              name="phosphorus"
              type="number"
              value={formData.phosphorus}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Potassium (K)"
              name="potassium"
              type="number"
              value={formData.potassium}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="pH"
              name="ph"
              type="number"
              value={formData.ph}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Temperature (°C)"
              name="temperature"
              type="number"
              value={formData.temperature}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Humidity (%)"
              name="humidity"
              type="number"
              value={formData.humidity}
              onChange={onChange}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              fullWidth
              label="Rainfall (mm)"
              name="rainfall"
              type="number"
              value={formData.rainfall}
              onChange={onChange}
            />
          </Grid>

          <Grid size={12}>
            <Stack direction="row" spacing={2}>
              <Button variant="contained" onClick={onSubmit} disabled={loading}>
                {loading ? "Analyzing..." : "Get Recommendation"}
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

export default SoilInputForm;