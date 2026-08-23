import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { Card, CardContent, Typography } from "@mui/material";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function CropBarChart({ data }) {
  const chartData = {
    labels: data.map((item) => item.crop),
    datasets: [
      {
        label: "Suitability Score",
        data: data.map((item) => item.score),
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
    },
  };

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Crop Suitability Chart
        </Typography>
        <Bar data={chartData} options={options} />
      </CardContent>
    </Card>
  );
}

export default CropBarChart;