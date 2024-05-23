<template>
  <el-row>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple">
        <h1>策略概览</h1>
        <h1>组合绩效</h1>
      </div>
    </el-col>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple-light">
        <h1>持仓总结</h1>
        <div ref="chartRef" style="width: 600px; height: 400px;"></div>
        <el-table :data="tableData" stripe style="width: 100%">
          <el-table-column prop="type" label="资产类型" width="180" />
          <el-table-column prop="money" label="市值" width="180" />
          <el-table-column prop="percent" label="市值占比" />
        </el-table>
        <h2 style="margin-top: 15px;">前五大持仓</h2>
      </div>
      <div>
        <el-table :data="topfive.value" stripe style="width: 100%">
            <el-table-column fixed prop="0" label="股票代码"  />
            <el-table-column prop="1.0" label="股票名称" />
            <el-table-column prop="1.1" label="单股价格"  />
            <el-table-column prop="1.2" label="持有数量" />
            <el-table-column prop="1.3" label="总价值" />
        </el-table>
      </div>
    </el-col>
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
  all_property: 0,
  stocks_held: undefined,
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
const topfive = reactive({
  value: [],
});
async function get_topfive() { // 获取前五大持仓
  const path = 'http://localhost:5000/home/topFive';
  try {
    const res = await axios.post(path, user.value);
    if (res.data.status === "success") {
      topfive.value = res.data.topFive;
      console.log('获取前五大持仓成功');
      console.log(topfive.value);
    } else {
      console.error('获取前五大持仓失败');
    }
  } catch (error) {
    console.error(error);
    console.error('网络问题，获取前五大持仓失败，请重试');
  }
}
onMounted(() => {
    get_topfive()
})


onMounted(() => {
  const chart = echarts.init(chartRef.value);
  const data = Object.entries(all_property).map(([name, value]) => ({ name, value }));
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