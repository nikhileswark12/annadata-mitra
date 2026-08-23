import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
} from "@mui/material";
import TaskAltRoundedIcon from "@mui/icons-material/TaskAltRounded";

function TreatmentSteps({ steps }) {
  return (
    <Card elevation={3} sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Treatment Recommendations
        </Typography>

        {steps && steps.length > 0 ? (
          <List sx={{ p: 0, mt: 1 }}>
            {steps.map((step, index) => (
              <ListItem
                key={index}
                sx={{
                  alignItems: "flex-start",
                  px: 0,
                  py: 1,
                  borderBottom:
                    index !== steps.length - 1 ? "1px solid #f0f0f0" : "none",
                }}
              >
                <ListItemIcon sx={{ minWidth: 36, mt: 0.3 }}>
                  <TaskAltRoundedIcon color="success" fontSize="small" />
                </ListItemIcon>

                <ListItemText
                  primary={
                    <Typography variant="body1" sx={{ lineHeight: 1.7 }}>
                      {step}
                    </Typography>
                  }
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Box
            sx={{
              minHeight: 180,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: "2px dashed #d9ead3",
              borderRadius: 2,
              backgroundColor: "#f8fff8",
              textAlign: "center",
              px: 2,
              mt: 1,
            }}
          >
            <Typography variant="body1" color="text.secondary">
              Treatment suggestions will appear here after analysis.
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default TreatmentSteps;