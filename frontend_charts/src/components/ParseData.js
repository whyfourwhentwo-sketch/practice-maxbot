
export const mockData = {
  // Данные для круговой диаграммы (настроение)
  mood: {
    labels: ['Позитивное', 'Нейтральное', 'Негативное'],
    values: [45, 30, 25],
    colors: ['#4CAF50', '#FFC107', '#F44336'],
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

const sentiment_labels = {
    positive: {value: "Позитивное", color: '#4CAF50'},
    neutral: {value: "Нейтральное", color: '#FFC107'},
    negative: {value: "Негативное", color: '#F44336'},
}

const generateColor = (index, total) => `hsl(${(index * 360 / total)}, 65%, 55%)`

export const ParseData = (api_response) => {
    console.log(api_response)
    const problems_total = api_response.problems.length;



    return ({

      // Данные для круговой диаграммы (настроение)
      mood: ({
        labels: Object.values(sentiment_labels).map(value => value.value),
        values: Object.keys(sentiment_labels).map(key => api_response.sentiment_pie[key]),
        colors: Object.values(sentiment_labels).map(value => value.color),
      }),

      // Данные для линейной диаграммы (изменение настроения по дням)
      moodDynamics: ({
        labels: api_response.sentiment_histogram.map(day => day.date.slice(5)),
        datasets: Object.keys(sentiment_labels).map(
            mood_label => ({
                label: sentiment_labels[mood_label].value,
                data: api_response.sentiment_histogram.map(day => day[mood_label]),
                borderColor: sentiment_labels[mood_label].color,
                backgroundColor: sentiment_labels[mood_label].color,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: sentiment_labels[mood_label].color,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
            })
        )
        
      }),

      // Данные для столбчатой диаграммы (проблемы)
      problems: ({
        labels: api_response.problems.map(problem => problem.category),
        values: api_response.problems.map(problem => problem.count),
        colors: api_response.problems.map((problem, i) => generateColor(i, problems_total)),
        total: problems_total // Общее количество обращений
      }),

      // Данные для топ-участников
      topUsers: ({
        active: api_response.top_users.most_active.map(user => ({
            name: user.user_name,
            messages: user.count
        })),
        positive: api_response.top_users.most_positive.map(user => ({
            name: user.user_name,
            messages: user.count
        })),
        negative: api_response.top_users.most_negative.map(user => ({
            name: user.user_name,
            messages: user.count
        })),
      })
    });

    
}


