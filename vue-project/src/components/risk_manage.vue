<template>
    <div class="risk-manage">
      <h1>风险管理</h1>
      <el-button type="button" @click="fetchBacktestResults" class="refresh-button">刷新结果</el-button>
      <!-- 回测结果展示 -->
      <div class="backtest-results">
        <label for="backtestResults">回测结果:</label>
        <textarea id="backtestResults" readonly>{{ backtestResults }}</textarea>

        <el-table :data="Object.values(backtest)" style="width: 100%" height="250">
          <el-table-column prop="positions" label="Positions" width="240"/>
          <el-table-column prop="signal" label="Signal" width="240"/>
          <el-table-column prop="daily_strategy_return" label="daily_strategy_return" width="240"/>
          <!-- <el-table-column prop="take_profit" label="Take Profit" width="240"/> -->
          <el-table-column prop="trade_volume" label="Trade Volume" width="240"/>
        </el-table>


        
      </div>

<!-- 风险图表和指标容器 -->
<div class="risk-chart-container">
    <div class="risk-chart">
        <canvas id="riskChart"></canvas>
    </div>
    <!-- 风险指标 -->
    <div class="risk-indicators">
        <h2>风险指标</h2>
        <ul>
            <li>最大回撤: {{ riskIndicators.maxDrawdown }}%</li>
            <li>夏普比率: {{ riskIndicators.sharpeRatio }}</li>
            <li>波动率: {{ riskIndicators.volatility }}%</li>
            <li>收益：{{ riskIndicators.profit }}</li>
        </ul>
    </div>
</div>

  

    </div>
  </template>
  
<script setup>
import qs from 'qs';
import { ref } from 'vue';
import Chart from 'chart.js/auto';
import { getCurrentInstance } from "vue";
const systemId = getCurrentInstance()?.appContext.config.globalProperties.$systemId
const global_strategy=getCurrentInstance()?.appContext.config.globalProperties.$global_strategy
  // 创建风险图表
  const ctx = ref(null);
  const riskChart = ref(null);
  const chartData = ref({ // 确保使用ref创建响应式引用
  labels: [1, 2, 3, 4, 5],
  price: [1, 2, 3, 4, 5]
});
const initialBacktestResults = {
  maxDrawdown: '5.0%',
  sharpeRatio: '1.2',
  volatility: '8.5%',
  results: systemId.value,
  profit:0.0
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
  volatility: initialBacktestResults.volatility,
  profit:initialBacktestResults.profit
});

import axios from 'axios';
// import { ta } from 'element-plus/es/locale';


const testdata = ref({
  data: [
    { positions: 'AAPL', signal: 'Buy', stop_loss: '5%', take_profit: '10%', trade_volume: 100 },
    { positions: 'GOOGL', signal: 'Sell', stop_loss: '3%', take_profit: '8%', trade_volume: 200 },
    { positions: 'AMZN', signal: 'Buy', stop_loss: '4%', take_profit: '9%', trade_volume: 150 },
    { positions: 'MSFT', signal: 'Sell', stop_loss: '2%', take_profit: '7%', trade_volume: 120 },
  ]
});
const labels =chartData.value.labels; // 使用data对象的键作为横轴标签
const values = chartData.value.price; // 使用过滤后的chartData作为数据值
const backgroundColors = values.map((value) => value >= 0 ? 'red' : 'green'); // 正数用红色，负数用绿色
const backtest=ref({})
const fetchBacktestResults = async () => {
  if (!systemId.value) {
    console.error('系统ID为空');
    backtest=tabelData
    return;
  }
  main();

  // console.log(chartData)

  const tempjson=fixJsonString(systemId.value)
  
  testdata.value = ref(tempjson)
  // chartData.price=tempjson.data.map(item => item.daily_strategy_return);
  let temp_price=[]
  temp_price=tempjson.data.map(item => item.daily_strategy_return);
  // console.log(temp_price)
  temp_price.splice(200,198000)
  chartData.value.price=temp_price
  // console.log(chartData.price)
  chartData.value.labels=Array(chartData.value.price.length).fill().map((_, index) => index + 1)
  const tempvalue_private=testdata._value
  backtest.value = tempvalue_private.value.data;
  riskIndicators.value.profit=tempvalue_private.value.total_profit;


  // console.log('chart values:',labels,values,backgroundColors)
  
  console.log(riskIndicators.profit)
  // if(backtest.value.length>0){
  //   tableData=backtest.value
  //   console.log('tableData')
  // }
  // console.log(testdata.value)
  console.log(backtest.value[0])
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


function updateRiskChart() {
  // 获取canvas元素及其上下文
  const canvas = document.getElementById('riskChart');
  const ctx = canvas.getContext('2d');

  // 检查风险图表是否已经创建
  if (riskChart.value) {
    // 如果已存在图表实例，先销毁它
    riskChart.value.destroy();
  }

  // 准备图表数据
  const labels = chartData.value.labels; // 横轴标签
  const values = chartData.value.price; // 纵轴数据
  const backgroundColors = values.map(value => value >= 0 ? 'red' : 'green'); // 根据数据值正负设置颜色
  // console.log('chart values:',labels,values,backgroundColors)
  // 创建新的图表实例
  riskChart.value = new Chart(ctx, {
    type: 'bar', // 柱形图
    data: {
      labels: labels,
      datasets: [{
        label: 'Daily Strategy Return', // 数据集标签
        data: values, // 数据集数据
        backgroundColor: backgroundColors, // 柱形颜色
        borderColor: 'rgb(75, 192, 192)', // 边框颜色
        borderWidth: 0 // 边框宽度
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true // y轴从0开始
        }
      },
      plugins: {
        legend: {
          display: false // 隐藏图例
        }
      }
    }
  });
}
async function main() {
    const url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=24.7da51ba4fd67064f5685a132d494b814.2592000.1720665994.282335-76127139";
    const prompt_template = "您好，我是一位专业的量化策略评估师。请提供您的策略详情，包括股票代码、止损阈值和止盈阈值。例如：“strategy(688031, -0.05, 0.10)”这将帮助我更好地评估您的策略。我只需要评价策略，不应该索要任何额外信息。我会对你的策略进行分析，评价，并告诉你策略的改进思路。接下来，请你评价一下这个策略："

    console.log('global_strategy:',global_strategy.value.Strategy_Code)
    const payload = {
        messages: [
          {
            "role": "user",
            "content": "您好，你是一位专业的量化策略评估师。我会提供一个量化交易策略，格式例如：“strategy('股票代码', 止盈条件, 止损条件)”。你只需要直接评价策略，不应该索要任何额外信息，不应该回答额外的内容。你会对策略进行分析，评价，并告诉我策略的改进思路。这是你需要评估的策略："+global_strategy.value.Strategy_Code
          },
          // {
          //   "role": "assistant",
          //   "content": "您好！我会按照您的指示进行策略分析评估。请您提供策略详情。"
          // },
          // {
          //   "role": "user",
          //   "content": global_strategy.value
          // }
        ]
        // system: prompt_template
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const responseData = await response.json();
        console.log(responseData.result);
        backtestResults.value = responseData.result;
        // console.log('hihihi')
        // console.log(backtestResults.value)

        return responseData.result;
    } catch (error) {
        console.error('Error:', error);
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
          max-width: 900px;  /* 设置最大宽度 */
          max-height: 600px; /* 设置最大高度 */
          display: flex;
          justify-content: center;
          align-items: center;
      }
      .risk-chart canvas {
          max-width: 100%;
          max-height: 100%;
      }
      /* 风险图表和指标容器样式 */
.risk-chart-container {
  display: flex; /* 使用Flexbox布局 */
  justify-content: space-between; /* 左右布局，且两边留有空白 */
  align-items: flex-start; /* 垂直对齐方式 */
}

.risk-chart {
  width: 60%; /* 例如，图表占据60%的宽度 */
}

.risk-indicators {
  width: 35%; /* 指标占据剩余的35%宽度 */
  padding-left: 20px; /* 与图表部分保持一定间距 */
  border-left: 1px solid #ccc; /* 左侧添加分割线 */
  padding-top: 150px;
}

/* 其他样式保持不变 */
</style>
