<template>
    <div class="risk-manage">
      <h1>风险管理</h1>
      <el-button type="button" @click="fetchBacktestResults" class="refresh-button">刷新结果</el-button>
      <!-- 回测结果展示 -->
      <div class="backtest-results">
        <label for="backtestResults">回测结果:</label>
        <textarea id="backtestResults" readonly>{{ backtestResults }}</textarea>
        <!-- <table>
          <thead>
            <tr>
              <th>Positions</th>
              <th>Signal</th>
              <th>Stop Loss</th>
              <th>Take Profit</th>
              <th>Trade Volume</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(trade, index) in backtest" :key="index">
              <td>{{ trade.positions }}</td>
              <td>{{ trade.signal }}</td>
              <td>{{ trade.stop_loss }}</td>
              <td>{{ trade.take_profit }}</td>
              <td>{{ trade.trade_volume }}</td>
            </tr>
          </tbody>
        </table> -->
        <el-table :data="Object.values(backtest)" style="width: 100%" height="250">
          <el-table-column prop="positions" label="Positions" width="240"/>
          <el-table-column prop="signal" label="Signal" width="240"/>
          <el-table-column prop="stop_loss" label="Stop Loss" width="240"/>
          <el-table-column prop="take_profit" label="Take Profit" width="240"/>
          <el-table-column prop="trade_volume" label="Trade Volume" width="240"/>
        </el-table>


        
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

      <!--as id=" 风险图表 -->
      <!-- <div class="risk-chart">
        <canvriskChart"></canvas>
      </div> -->
  

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
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-08',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-06',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
  {
    date: '2016-05-07',
    name: 'Tom',
    state: 'California',
    city: 'Los Angeles',
    address: 'No. 189, Grove St, Los Angeles',
    zip: 'CA 90036',
  },
]
// 使用ref来创建可变的响应式数据对象
const backtestResults = ref(initialBacktestResults.results);
const riskIndicators = ref({
  maxDrawdown: initialBacktestResults.maxDrawdown,
  sharpeRatio: initialBacktestResults.sharpeRatio,
  volatility: initialBacktestResults.volatility
});

import axios from 'axios';
// import { ta } from 'element-plus/es/locale';
const data={
  maxDrawdown: '4.8%',
  sharpeRatio: '1.3',
  volatility: '7.9%',
  results: '更新后的回测结果详细文本...',
  labels: ['1月', '2月', '3月', '4月', '5月'],
  price: [10, 20, 15, 25, 30]
};

const testdata = ref({
  data: [
    { positions: 'AAPL', signal: 'Buy', stop_loss: '5%', take_profit: '10%', trade_volume: 100 },
    { positions: 'GOOGL', signal: 'Sell', stop_loss: '3%', take_profit: '8%', trade_volume: 200 },
    { positions: 'AMZN', signal: 'Buy', stop_loss: '4%', take_profit: '9%', trade_volume: 150 },
    { positions: 'MSFT', signal: 'Sell', stop_loss: '2%', take_profit: '7%', trade_volume: 120 },
  ]
});
const tpstring="{\n  \"data\": [\n    {\n      \"positions\": NaN,\n      \"signal\": 0.0,\n      \"stop_loss\": 0.0,\n      \"take_profit\": 0.0,\n      \"trade_volume\": 100\n    },\n    {\n      \"positions\": 0.0,\n      \"signal\": 0.0,\n      \"stop_loss\": 0.0,\n      \"take_profit\": 0.0,\n      \"trade_volume\": 0\n    }\n ],\n  \"status\": \"success\"\n}\n"

const backtest=ref({})
const fetchBacktestResults = async () => {
  if (!systemId.value) {
    console.error('系统ID为空');
    backtest=tabelData
    return;
  }
  const tempjson=fixJsonString(systemId.value)
  testdata.value = ref(tempjson)
  const tempvalue_private=testdata._value
  backtest.value = tempvalue_private.value.data;
  // if(backtest.value.length>0){
  //   tableData=backtest.value
  //   console.log('tableData')
  // }
  // console.log(testdata.value)
  console.log(backtest.value)
  console.log(typeof testdata.value)
  updateRiskChart();
  };
function fixJsonString(jsonString) {
  // 将字符串中的NaN替换为"NaN"
  let fixedString = jsonString.replace(/NaN/g, '"NaN"');

  // 使用JSON.parse来解析字符串，这将自动处理未被双引号包围的值
  try {
    const parsedData = JSON.parse(fixedString);
    return parsedData; // 如果没有错误，返回解析后的对象
  } catch (error) {
    // 如果解析失败，抛出错误
    console.error('Error parsing JSON string:', error);
    throw error;
  }
}
  
  // 创建风险图表
  const ctx = ref(null);
  const riskChart = ref(null);
  
// onMounted(() => {
//   ctx.value = document.getElementById('riskChart').getContext('2d');
//   riskChart.value = new Chart(ctx.value, {
//     type: 'line', // 这里可以根据需要更改图表类型
//     data: {
//       // 这里是图表的数据，可以根据实际数据进行填充
//       labels:data.labels,
//       datasets: [{
//         label: '风险指标',
//         data: data.price,
//         fill: false,
//         borderColor: 'rgb(75, 192, 192)',
//         tension: 0.1
//       }]
//     },
//     options: {
//       // 图表配置项
//       scales: {
//         y: {
//           beginAtZero: false
//         }
//       }
//     }
//   });
// });
  
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
