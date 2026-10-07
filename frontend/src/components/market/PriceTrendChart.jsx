import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const PriceTrendChart = ({ trends }) => {
  const data = {
    labels: trends.map((t) => t.label),
    datasets: [
      {
        label: "Market Price (₹)",
        data: trends.map((t) => t.value),
      },
    ],
  };

  return <Bar data={data} />;
};

export default PriceTrendChart;