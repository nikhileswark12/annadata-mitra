import { Chip } from "@mui/material";

const statusColors = {
  healthy: "success",
  low: "success",
  medium: "warning",
  high: "error",
  critical: "error",
  processing: "info",
  active: "success",
  inactive: "default",
};

function StatusChip({ status, label, ...props }) {
  const normalizedStatus = status?.toLowerCase() || "default";
  const color = statusColors[normalizedStatus] || "default";
  
  return (
    <Chip
      label={label || status}
      color={color}
      sx={{ fontWeight: 700, width: "fit-content" }}
      {...props}
    />
  );
}

export default StatusChip;
