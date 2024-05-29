<template>
    <div class="risk-manage">
      <h1>风险管理</h1>
      
      <!-- 回测结果展示 -->
      <div class="backtest-results">
        <label for="backtestResults">回测结果:</label>
        <textarea id="backtestResults" readonly>{{ backtestResults }}</textarea>
      </div>
  
      <!-- 风险指标 -->
      <div class="risk-indicators">
        <h2>风险指标</h2>
        <ul>
          <li>最大回撤: {{ riskIndicators.maxDrawdown }}%</li>
          <li>夏普比率: {{ riskIndicators.sharpeRatio }}</li>
          <li>波动率: {{ riskIndicators.volatility }}%</li>
        </ul>
      </div>
  
      <!-- 风险图表 -->
      <div class="risk-chart">
        <canvas id="riskChart"></canvas>
      </div>
  
      <!-- 刷新按钮 -->
      <button type="button" @click="fetchBacktestResults" class="refresh-button">刷新结果</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import Chart from 'chart.js/auto';
  
  // 假设这是从API获取的回测结果数据
  const initialBacktestResults = {
    maxDrawdown: '5.0%',
    sharpeRatio: '1.2',
    volatility: '8.5%',
    results: '这里是回测结果的详细文本...'
  };
  
  // 使用ref来创建可变的响应式数据对象
  const backtestResults = ref(initialBacktestResults.results);
  const riskIndicators = ref({
    maxDrawdown: initialBacktestResults.maxDrawdown,
    sharpeRatio: initialBacktestResults.sharpeRatio,
    volatility: initialBacktestResults.volatility
  });
  
  const fetchBacktestResults = async() => {
    // 这里应该是API请求获取回测结果的逻辑
    // 模拟API响应
    const mockApiResponse = {
      maxDrawdown: '4.8%',
      sharpeRatio: '1.3',
      volatility: '7.9%',
      results: '更新后的回测结果详细文本...'
    };
    
    backtestResults.value = mockApiResponse.results;
    riskIndicators.value = {
      maxDrawdown: mockApiResponse.maxDrawdown,
      sharpeRatio: mockApiResponse.sharpeRatio,
      volatility: mockApiResponse.volatility
    };
    
    // 更新风险图表
    updateRiskChart();
  };
  
  // 创建风险图表
  const ctx = ref(null);
  const riskChart = ref(null);
  
  onMounted(() => {
    ctx.value = document.getElementById('riskChart').getContext('2d');
    riskChart.value = new Chart(ctx.value, {
      type: 'line', // 这里可以根据需要更改图表类型
      data: {
        // 这里是图表的数据，可以根据实际数据进行填充
        labels: ['1月', '2月', '3月', '4月', '5月'],
        datasets: [{
          label: '风险指标',
          data: [10, 20, 15, 25, 30],
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      },
      options: {
        // 图表配置项
        scales: {
          y: {
            beginAtZero: false
          }
        }
      }
    });
  });
  
  function updateRiskChart() {
    if (riskChart.value) {
      // 这里可以根据实际的风险指标数据更新图表
      // 示例：更新数据集的数据
      riskChart.value.data.datasets[0].data = [10, 20, 15, 25, 30]; // 假设数据
    }
  }
  </script>
  
  <style scoped>
  .risk-manage {
    display: flex;
    flex-direction: column;
  }
  .backtest-results textarea, .risk-indicators ul, .risk-chart canvas {
    margin-bottom: 20px;
  }
  .backtest-results textarea {
    width: 100%;
    height: 200px;
  }
  .risk-indicators ul {
    list-style-type: none;
    padding: 0;
  }
  .risk-indicators li {
    padding: 5px 0;
  }
  .refresh-button {
    margin-top: 20px;
  }
  </style>