<template>
    <el-row>
    <el-col :span="12"><div class="grid-content ep-bg-purple">
        <h1>策略概览</h1>
        <h1>组合绩效</h1>
        </div>
    </el-col>
    <el-col :span="12"><div class="grid-content ep-bg-purple-light">
        <h1>持仓总结</h1>
        <div ref="chartRef" style="width: 600px; height: 400px;"></div>
        <el-table :data="tableData" stripe style="width: 100%">
    <el-table-column prop="type" label="资产类型" width="180" />
    <el-table-column prop="money" label="市值" width="180" />
    <el-table-column prop="percent" label="市值占比" />
  </el-table>
  <h2 style="margin-top: 15px;">前五大持仓</h2>
    </div></el-col>
  </el-row>
</template>

<script setup>
import { ref, reactive } from 'vue';
import * as echarts from 'echarts';
import { useStorage } from '@vueuse/core';
import axios from 'axios'; // 导入 axios 库，用于发送 HTTP 请求
const user = useStorage('user', ({
    name: '',
    remember: false,
    password: '',
    account: '',
    balance: 1000000,
    stocks_held: [{'code': '000001', 'place': 'cn', 'amount': 1000}, 
    {'code': '603000', 'place': 'cn', 'amount': 2000}
    ],
}));
const chartRef = ref(null);
const all_property = reactive({ //理论上，应该由后端根据用户持股来转换，而不是我在这里写死
    A股: 1000,
    美股: 500,
    港股: 200,
})
const total = computed(() => Object.values(all_property).reduce((a, b) => a + b, 0));
const tableData = reactive([
    { type: 'A股', money: all_property.A股, percent: computed(() => (all_property.A股 / total.value * 100).toFixed(2) + '%') },
    { type: '美股', money: all_property.美股, percent: computed(() => (all_property.美股 / total.value * 100).toFixed(2) + '%') },
    { type: '港股', money: all_property.港股, percent: computed(() => (all_property.港股 / total.value * 100).toFixed(2) + '%') },
  ]);

onMounted(() => {
  const chart = echarts.init(chartRef.value);
  const data = Object.entries(all_property).map(([name, value]) => ({name, value}));
  chart.setOption({
    title: {
      text: '资产分布',
      left: 'center'
    },
    series: [{
      type: 'pie',
      data: data,
      label: {
        formatter: '{b}: {c} ({d}%)'
      }
    }]
  });
});
</script>

<style lang="scss" scoped>
h1 {
    font-size: 24px;
}

h2 {
    font-size: 20px;
}
</style>