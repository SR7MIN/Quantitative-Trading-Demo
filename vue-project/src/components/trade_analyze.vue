<template>
  <h1 style="margin-top: 15px;">您持有的股票的盈亏情况见下表：</h1>
  <div v-loading="isLoading">
    <el-table :data="all_stock" stripe style="width: 100%">
      <el-table-column prop="code" label="股票代码" width="180" />
      <el-table-column prop="name" label="股票名称" width="180" />
      <el-table-column prop="num" label="持有数目" />
      <el-table-column prop="price" label="单股价格" />
      <!-- // 涨跌幅 -->
      <el-table-column prop="percent" label="涨跌幅(%)" />
      <el-table-column prop="total" label="净利润" />

    </el-table>
    <el-row style="margin-top: 30px;">
      <el-col :span="12">
        <div ref="chartRef" style="width: 600px; height: 400px;"></div>
      </el-col>
      <el-col :span="12">
        <div ref="chartRef2" style="width: 600px; height: 400px;"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted} from 'vue'
import { useStorage } from '@vueuse/core'
import axios from 'axios';
import * as echarts from 'echarts';
const chartRef = ref(null);
const chartRef2 = ref(null);
const user = useStorage('user', {
  name: '',
  remember: false,
  password: '',
  account: '',
  balance: 1000000,
  all_property: 0,
  stocks_held: undefined,
})
const stock_Data = ref([])
const isLoading = computed(() => stock_Data.value.length === 0);
//查询用户的持股情况
const all_stock = computed(() => {
  return Object.values(stock_Data.value).map(stock => {
    return {
      code: stock[0],
      name: stock[1],
      num: stock[2],
      price: stock[3],
      percent: stock[4],
      total: (stock[2] * stock[3] * stock[4] * 0.01).toFixed(2) // 这里假设净利润是数目乘以价格
    }
  })
});
async function get_stock() {
  const path = 'http://localhost:5000/home/held-stock'
  try {
    const res = await axios.post(path, user.value)
    if (res.data.status === 'success') {
      stock_Data.value = res.data.stocks_info
      console.log('获取用户持股成功')
      console.log(stock_Data.value)
    } else {
      console.error('获取用户持股失败')
    }
  } catch (error) {
    console.error(error)
    console.error('网络问题，获取用户持股失败，请重试')
  }
}
onMounted(async () => {
  await get_stock();
  const chart = echarts.init(chartRef.value);
  chart.setOption({
    title: {
      text: '股票净利润'
    },
    tooltip: {},
    xAxis: {
      data: all_stock.value.map(stock => stock.name)
    },
    yAxis: {},
    series: [{
      name: '净利润',
      type: 'bar',
      data: all_stock.value.map(stock => stock.total),
      itemStyle: {
        color: function(params) {
          return params.data > 0 ? 'red' : 'green';
        }
      }
    }]
  });
  const chart2 = echarts.init(chartRef2.value);
  chart2.setOption({
    title: {
      text: '持股数量'
    },
    tooltip: {},
    series: [{
      name: '持股数量',
      type: 'pie',
      radius: ['50%', '70%'], // 这使得图表成为一个环形图
      data: all_stock.value.map(stock => ({
        name: stock.name,
        value: stock.num
      })),
      itemStyle: {
        emphasis: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  });
});
</script>

<style lang="scss" scoped></style>
