import {
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Chart as ChartJS,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function CropSuitabilityChart({ data }) {
  const chartData = {
    labels: data.map((item) => item.crop),
    datasets: [
      {
        label: "Suitability (%)",
        data: data.map((item) => item.suitability),
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
  };

  return <Bar data={chartData} options={options} />;
}

export default CropSuitabilityChart;