import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const data = {
  labels: ['Электроника', 'Одежда', 'Книги', 'Дом и сад', 'Спорт'],
  datasets: [
    {
      data: [45, 32, 21, 28, 15],
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
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

function PieChart() {
  return (
    <div style={{ 
      maxWidth: '500px', 
      margin: '30px auto', 
      padding: '30px', 
      background: 'white', 
      borderRadius: '15px', 
      boxShadow: '0 4px 20px rgba(0,0,0,0.1)' 
    }}>
      <h3 style={{ textAlign: 'center', color: '#2c3e50', marginBottom: '20px' }}>
        🍩 Распределение по категориям
      </h3>
      <div style={{ height: '300px' }}>
        <Pie data={data} />
      </div>
    </div>
  );
}

export default PieChart;