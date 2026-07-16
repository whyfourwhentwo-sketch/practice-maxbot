import React, { useState } from 'react';
import { Pie, Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './Dashboard.css';
import ParseData from './ParseData';

// Регистрируем компоненты Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// 📌 ДАННЫЕ-ЗАГЛУШКА
const mockData = {
  // Данные для круговой диаграммы (настроение)
  mood: {
    labels: ['Позитивное', 'Нейтральное', 'Негативное'],
    values: [45, 30, 25],
    colors: ['#4CAF50', '#FFC107', '#F44336'],
    dateRange: {
      from: '2026-07-01',
      to: '2026-07-14'
    }
  },
  // Данные для линейной диаграммы (изменение настроения по дням)
  moodDynamics: {
    labels: ['01.07', '02.07', '03.07', '04.07', '05.07', '06.07', '07.07', '08.07', '09.07', '10.07', '11.07', '12.07', '13.07', '14.07'],
    datasets: [
      {
        label: 'Позитивное',
        data: [42, 48, 45, 52, 38, 55, 60, 42, 48, 52, 45, 50, 55, 58],
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#4CAF50',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
      },
      {
        label: 'Нейтральное',
        data: [30, 28, 32, 25, 35, 30, 25, 32, 28, 30, 35, 28, 30, 28],
        borderColor: '#FFC107',
        backgroundColor: 'rgba(255, 193, 7, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#FFC107',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
      },
      {
        label: 'Негативное',
        data: [28, 24, 23, 23, 27, 15, 15, 26, 24, 18, 20, 22, 15, 14],
        borderColor: '#F44336',
        backgroundColor: 'rgba(244, 67, 54, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#F44336',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
      },
    ]
  },
  // Данные для столбчатой диаграммы (проблемы)
  problems: {
    labels: ['Сломанный лифт', 'Отсутствие воды', 'Проблемы с отоплением', 'Вывоз мусора', 'Плохое освещение', 'Канализация'],
    values: [42, 38, 25, 30, 18, 22],
    colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#DDA0DD'],
    total: 175 // Общее количество обращений
  },
  // Данные для топ-участников
  topUsers: {
    active: [
      { name: 'Алексей С.', messages: 156 },
      { name: 'Мария И.', messages: 142 },
      { name: 'Дмитрий К.', messages: 128 },
      { name: 'Елена В.', messages: 115 },
      { name: 'Сергей П.', messages: 98 },
    ],
    positive: [
      { name: 'Мария И.', messages: 89 },
      { name: 'Алексей С.', messages: 76 },
      { name: 'Елена В.', messages: 68 },
      { name: 'Дмитрий К.', messages: 55 },
      { name: 'Ольга Н.', messages: 48 },
    ],
    negative: [
      { name: 'Сергей П.', messages: 42 },
      { name: 'Алексей С.', messages: 35 },
      { name: 'Дмитрий К.', messages: 28 },
      { name: 'Иван Р.', messages: 25 },
      { name: 'Мария И.', messages: 18 },
    ]
  }
};

function Dashboard() {
  const [chatId, setChatId] = useState('');
  const [platform, setPlatform] = useState('telegram');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [data, setData] = useState(mockData);


  const handleShowResults = async () => {
    if (!chatId) {
      alert('Пожалуйста, введите ID чата');
      return;
    }
    if (!startDate || !endDate) {
      alert('Пожалуйста, выберите даты');
      return;
    }
    let response = await fetch(`http://127.0.0.1:5000/stats?chat_id=${chatId}`)
    if(response.ok){
      let json = await response.json()
      console.log(json)
      setData(ParseData(json))
      
    }
    setShowResults(true);
  };

  // Конфигурация круговой диаграммы (настроение)
  const pieChartData = {
    labels: data.mood.labels,
    datasets: [
      {
        data: data.mood.values,
        backgroundColor: data.mood.colors,
        borderColor: '#fff',
        borderWidth: 3,
        hoverOffset: 8,
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          font: { size: 13, weight: '600' },
          color: '#2c3e50',
          padding: 16,
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let total = context.dataset.data.reduce((a, b) => a + b, 0);
            let percentage = ((context.parsed / total) * 100).toFixed(1);
            return `${context.label}: ${percentage}% (${context.parsed} чел.)`;
          }
        }
      }
    },
  };

  // Конфигурация линейной диаграммы (изменение настроения по дням)
  const lineChartData = {
    labels: data.moodDynamics.labels,
    datasets: data.moodDynamics.datasets,
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: { size: 12, weight: '600' },
          color: '#2c3e50',
          usePointStyle: true,
          pointStyle: 'circle',
          padding: 16,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y}%`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        grid: { color: 'rgba(0,0,0,0.06)' },
        ticks: { 
          font: { size: 11 },
          callback: function(value) {
            return value + '%';
          }
        },
      },
      x: {
        grid: { display: false },
        ticks: { 
          font: { size: 11 },
          maxTicksLimit: 14,
        },
      },
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
  };

  // Конфигурация столбчатой диаграммы (проблемы)
  const barChartData = {
    labels: data.problems.labels,
    datasets: [
      {
        label: 'Количество обращений',
        data: data.problems.values,
        backgroundColor: data.problems.colors,
        borderColor: data.problems.colors.map(c => c),
        borderWidth: 2,
        borderRadius: 6,
        maxBarThickness: 40,
      },
    ],
  };

  const barOptions = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.parsed.x} обращений`;
          }
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: { color: 'rgba(0,0,0,0.06)' },
        ticks: { font: { size: 12 } },
      },
      y: {
        grid: { display: false },
        ticks: { 
          font: { size: 13, weight: '500' },
          color: '#2c3e50',
        },
      },
    },
  };

  return (
    <div className="dashboard">
      {/* Блок с фильтрами */}
      <div className="filters-block">
        <div className="filters-grid">
          <div className="filter-item">
            <label className="filter-label">ID чата</label>
            <input
              type="text"
              className="filter-input"
              placeholder="Введите ID чата"
              value={chatId}
              onChange={(e) => setChatId(e.target.value)}
            />
          </div>

          <div className="filter-item">
            <label className="filter-label">Платформа</label>
            <div className="platform-group">
              <button
                className={`platform-btn ${platform === 'telegram' ? 'active' : ''}`}
                onClick={() => setPlatform('telegram')}
              >
                Telegram
              </button>
              <button
                className={`platform-btn ${platform === 'max' ? 'active' : ''}`}
                onClick={() => setPlatform('max')}
              >
                MAX
              </button>
            </div>
          </div>

          <div className="filter-item">
            <label className="filter-label">Период</label>
            <div className="date-group">
              <input
                type="date"
                className="date-input"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
              <span className="date-sep">—</span>
              <input
                type="date"
                className="date-input"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>

          <div className="filter-item filter-action">
            <button className="show-btn" onClick={handleShowResults}>
              Показать результаты
            </button>
          </div>
        </div>
      </div>

      {/* Блок с графиками */}
      {showResults && (
        <div className="results-block">
          {/* Верхняя строка - два графика рядом */}
          <div className="charts-row">
            {/* Первый график - Круговая диаграмма настроения */}
            <div className="chart-wrapper pie-chart-wrapper">
              <div className="chart-header">
                <div className="chart-title-group">
                  <h3 className="chart-title">Распределение настроений</h3>
                  
                </div>
              </div>
              <div className="chart-body pie-chart-body">
                <Pie data={pieChartData} options={pieOptions} />
              </div>
            </div>

            {/* Второй график - Линейная диаграмма изменения настроения по дням */}
            <div className="chart-wrapper line-chart-wrapper">
              <div className="chart-header">
                <h3 className="chart-title">Изменение эмоционального окраса по дням</h3>
              </div>
              <div className="chart-body line-chart-body">
                <Line data={lineChartData} options={lineOptions} />
              </div>
            </div>
          </div>

          {/* Третий график - Столбчатая диаграмма проблем с общим количеством */}
          <div className="chart-wrapper bar-chart-wrapper">
            <div className="chart-header">
              <div className="chart-title-group">
                <h3 className="chart-title">Количество обращений по проблемам</h3>
                <span className="chart-total-badge">
                  Всего: {data.problems.total} обращений
                </span>
              </div>
            </div>
            <div className="chart-body bar-chart-body">
              <Bar data={barChartData} options={barOptions} />
            </div>
          </div>

          {/* Блок с топ-участниками */}
          <div className="top-users-section">
            <h3 className="top-users-title">Топ активных участников</h3>
            <div className="top-users-grid">
              {/* Список 1: Самые активные пользователи */}
              <div className="top-users-card">
                <h4 className="top-users-card-title">Самые активные</h4>
                <div className="top-users-list">
                  {data.topUsers.active.map((user, index) => (
                    <div key={index} className="top-user-item">
                      <span className="top-user-rank">{index + 1}</span>
                      <span className="top-user-name">{user.name}</span>
                      <span className="top-user-count">{user.messages} сообщ.</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Список 2: Самые позитивные пользователи */}
              <div className="top-users-card positive">
                <h4 className="top-users-card-title">Самые позитивные</h4>
                <div className="top-users-list">
                  {data.topUsers.positive.map((user, index) => (
                    <div key={index} className="top-user-item">
                      <span className="top-user-rank">{index + 1}</span>
                      <span className="top-user-name">{user.name}</span>
                      <span className="top-user-count">{user.messages} сообщ.</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Список 3: Самые негативные пользователи */}
              <div className="top-users-card negative">
                <h4 className="top-users-card-title">Самые негативные</h4>
                <div className="top-users-list">
                  {data.topUsers.negative.map((user, index) => (
                    <div key={index} className="top-user-item">
                      <span className="top-user-rank">{index + 1}</span>
                      <span className="top-user-name">{user.name}</span>
                      <span className="top-user-count">{user.messages} сообщ.</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;