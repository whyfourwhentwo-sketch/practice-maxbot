import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Регистрируем модули Chart.js (обязательно!)
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// Данные-заглушка
const data = {
  labels: ['Электроника', 'Одежда', 'Книги', 'Дом и сад', 'Спорт'],
  datasets: [
    {
      label: 'Выручка (тыс. ₽)',
      data: [45, 32, 21, 28, 15],
      backgroundColor: [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 2,
    },
  ],
};

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: '📊 Статистика продаж по категориям',
      font: {
        size: 18,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
    },
  },
};

function MyChart() {
  return (
    <div style={{ 
      maxWidth: '800px', 
      margin: '50px auto', 
      padding: '30px', 
      background: 'white', 
      borderRadius: '15px', 
      boxShadow: '0 4px 20px rgba(0,0,0,0.1)' 
    }}>
      <div style={{ height: '400px' }}>
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}

export default MyChart;