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
        backgroundColor: "#2e7d32",
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context) => `Suitability: ${context.parsed.y}%`
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Suitability (%)'
        }
      }
    }
  };

  return (
    <div style={{ height: "300px", position: "relative" }}>
      <Bar data={chartData} options={options} />
    </div>
  );
}

export default CropSuitabilityChart;