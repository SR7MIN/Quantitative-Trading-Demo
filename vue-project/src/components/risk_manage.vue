<template>
    <div class="risk-manage">
      <h1>风险管理</h1>
      <el-button type="button" @click="fetchBacktestResults" class="refresh-button">刷新结果</el-button>
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
  

    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import Chart from 'chart.js/auto';
  import { getCurrentInstance } from "vue";
  const systemId = getCurrentInstance()?.appContext.config.globalProperties.$systemId
  // 假设这是从API获取的回测结果数据
  const initialBacktestResults = {
    maxDrawdown: '5.0%',
    sharpeRatio: '1.2',
    volatility: '8.5%',
    results: systemId.value,
  };
  
  // 使用ref来创建可变的响应式数据对象
  const backtestResults = ref(initialBacktestResults.results);
  const riskIndicators = ref({
    maxDrawdown: initialBacktestResults.maxDrawdown,
    sharpeRatio: initialBacktestResults.sharpeRatio,
    volatility: initialBacktestResults.volatility
  });
  
  import axios from 'axios';
const data={
  maxDrawdown: '4.8%',
  sharpeRatio: '1.3',
  volatility: '7.9%',
  results: '更新后的回测结果详细文本...',
  labels: ['1月', '2月', '3月', '4月', '5月'],
  price: [10, 20, 15, 25, 30]
}




const fetchBacktestResults = async () => {
  console.log(systemId)
  try {
    // 这里替换为实际的API请求获取回测结果的逻辑
    const response = await axios.get('http://localhost:5000/api/backtest-results');
    const data = response.data;
    
    if (data && data.results) {
      // 如果API响应包含数据，则更新回测结果和风险指标
      backtestResults.value = data.results;
      riskIndicators.value = {
        maxDrawdown: data.maxDrawdown,
        sharpeRatio: data.sharpeRatio,
        volatility: data.volatility
      };
    } else {
      // 如果API响应不包含数据，则使用模拟数据
      throw new Error('No data received');
    }

    // 更新风险图表
    updateRiskChart();
  } catch (error) {
    // 如果发生错误或没有接收到数据，使用模拟数据
    console.error('获取回测结果失败:', error);
    backtestResults.value = '更新后的回测结果详细文本...';
    riskIndicators.value = {
      maxDrawdown: '4.8%',
      sharpeRatio: '1.3',
      volatility: '7.9%'
    };
    // 可以选择在这里更新风险图表或跳过
    updateRiskChart();
  }
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
        labels:data.labels,
        datasets: [{
          label: '风险指标',
          data: data.price,
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
      riskChart.value.data.datasets[0].data = data.price;
      
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

  body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .header, .content {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header button {
            background-color: #007BFF;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .header button:hover {
            background-color: #0056b3;
        }
        .content {
            display: flex;
            gap: 20px;
        }
        .code-editor, .markdown-editor {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .code-editor textarea, .markdown-editor textarea {
            width: 100%;
            height: 200px;
            font-family: 'Courier New', Courier, monospace;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            resize: none;
        }
        .markdown-preview {
            background-color: #f9f9f9;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .risk-chart {
            margin-top: 20px;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;  /* 设置最大宽度 */
            max-height: 400px; /* 设置最大高度 */
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .risk-chart canvas {
            max-width: 100%;
            max-height: 100%;
        }
  </style>