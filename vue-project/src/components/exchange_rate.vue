<template>
  <div>
    <h1>今日汇率中间价市场</h1>
    <el-table :data="[todayrate]" style="width: 100%">
      <el-table-column prop="美元" label="美元" />
      <el-table-column prop="欧元" label="欧元" />
      <el-table-column prop="日元" label="日元" />
      <el-table-column prop="港元" label="港元" />
      <el-table-column prop="英镑" label="英镑" />
      <el-table-column prop="卢布" label="卢布" />
    </el-table>
    <el-row>
      <el-col :span="12">
        <div ref="chartRef1" style="width: 600px; height: 400px" v-loading="isLoading"></div>
        <div ref="chartRef2" style="width: 600px; height: 400px"></div>
        <div ref="chartRef5" style="width: 600px; height: 400px"></div>
      </el-col>
      <el-col :span="12">
        <div ref="chartRef3" style="width: 600px; height: 400px" v-loading="isLoading2"></div>
        <div ref="chartRef4" style="width: 600px; height: 400px"></div>
        <div ref="chartRef6" style="width: 600px; height: 400px"></div>
      </el-col>
    </el-row>

  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
// import { ElLoading, ElMessage, ElMessageBox } from 'element-plus';
import { onMounted } from 'vue'
import { useStorage } from '@vueuse/core'
const rate = ref([])
const todayrate = ref([])
const chartRef1 = ref(null)
const chartRef2 = ref(null)
const chartRef3 = ref(null)
const chartRef4 = ref(null)
const chartRef5 = ref(null)
const chartRef6 = ref(null)
const isLoading = computed(() => rate.value.length === 0);
const isLoading2 = computed(() => rate.value.length === 0);
async function get_rate() {
  // 查询外汇市场
  const path = 'http://localhost:5000/home/foreign-exchange'
  try {
    const res = await axios.post(path, rate.value)
    if (res.data.status === 'success') {
      console.log('get rate success')
      rate.value = res.data.data
      todayrate.value = rate.value[rate.value.length - 1]
      console.log(rate.value)
      console.log(todayrate.value)
    } else {
      // handle login failure
      console.error('get rate failed')
    }
  } catch (error) {
    console.error(error)
  }
}

onMounted(
  async () => {
    await get_rate()
    const chart1 = echarts.init(chartRef1.value)
    const chart2 = echarts.init(chartRef2.value)
    const chart3 = echarts.init(chartRef3.value)
    const chart4 = echarts.init(chartRef4.value)
    const chart5 = echarts.init(chartRef5.value)
    const chart6 = echarts.init(chartRef6.value)
    const usdRates = rate.value.map((item) => item.美元)
    const eurRates = rate.value.map((item) => item.欧元)
    const jpyRates = rate.value.map((item) => item.日元)
    const gbpRates = rate.value.map((item) => item.英镑)
    const hkdRates = rate.value.map((item) => item.港元)
    const rusaRates = rate.value.map((item) => item.卢布)
    const dates = rate.value.map((item) => {
      const date = new Date(item.日期)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      })
    })
    chart1.setOption({
      title: {
        text: `美元对人民币的中间价走势`,
      },

      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
        },
        {
          type: 'inside',
        },
      ],
      xAxis: {
        data: dates,
        type: 'category',
        name: '日期',
      },
      yAxis: {
        type: 'value',
        min: Math.min(...usdRates),
        max: Math.max(...usdRates),
        name: '收盘价',
      },
      series: [
        {
          name: '收盘价',
          type: 'line',
          data: usdRates,
        },
      ],
    })
    chart2.setOption({
      title: {
        text: `欧元对人民币的中间价走势`,
      },

      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
        },
        {
          type: 'inside',
        },
      ],
      xAxis: {
        data: dates,
        type: 'category',
        name: '日期',
      },
      yAxis: {
        type: 'value',
        min: Math.min(...eurRates),
        max: Math.max(...eurRates),
        name: '收盘价',
      },
      series: [
        {
          name: '收盘价',
          type: 'line',
          data: eurRates,
        },
      ],
    })
    chart3.setOption({
      title: {
        text: `日元对人民币的中间价走势`,
      },

      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
        },
        {
          type: 'inside',
        },
      ],
      xAxis: {
        data: dates,
        type: 'category',
        name: '日期',
      },
      yAxis: {
        type: 'value',
        min: Math.min(...jpyRates),
        max: Math.max(...jpyRates),
        name: '收盘价',
      },
      series: [
        {
          name: '收盘价',
          type: 'line',
          data: jpyRates,
        },
      ],
    })
    chart4.setOption({
      title: {
        text: `英镑对人民币的中间价走势`,
      },

      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
        },
        {
          type: 'inside',
        },
      ],
      xAxis: {
        data: dates,
        type: 'category',
        name: '日期',
      },
      yAxis: {
        type: 'value',
        min: Math.min(...gbpRates),
        max: Math.max(...gbpRates),
        name: '收盘价',
      },
      series: [
        {
          name: '收盘价',
          type: 'line',
          data: gbpRates,
        },
      ],
    })
    chart5.setOption({
      title: {
        text: `港元对人民币的中间价走势`,
      },

      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
        },
        {
          type: 'inside',
        },
      ],
      xAxis: {
        data: dates,
        type: 'category',
        name: '日期',
      },
      yAxis: {
        type: 'value',
        min: Math.min(...hkdRates),
        max: Math.max(...hkdRates),
        name: '收盘价',
      },
      series: [
        {
          name: '收盘价',
          type: 'line',
          data: hkdRates,
        },
      ],
    })
    chart6.setOption({
      title: {
        text: `卢布对人民币的中间价走势`,
      },

      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      dataZoom: [
        {
          type: 'slider',
          start: 0,
          end: 100,
        },
        {
          type: 'inside',
        },
      ],
      xAxis: {
        data: dates,
        type: 'category',
        name: '日期',
      },
      yAxis: {
        type: 'value',
        min: Math.min(...rusaRates),
        max: Math.max(...rusaRates),
        name: '收盘价',
      },
      series: [
        {
          name: '收盘价',
          type: 'line',
          data: rusaRates,
        },
      ],
    })

  }
)
// chart = echarts.init(chartRef.value)
//           const dates = stock.data.map((item) => {
//             const date = new Date(item.日期)
//             return date.toLocaleDateString('zh-CN', {
//               year: 'numeric',
//               month: '2-digit',
//               day: '2-digit',
//             })
//           })
//           chart.setOption({
//             title: {
//               text: `近一年历史股价 - ${stock.name}`,
//             },

//             tooltip: {
//               trigger: 'axis',
//               axisPointer: {
//                 type: 'cross',
//               },
//             },
//             dataZoom: [
//               {
//                 type: 'slider',
//                 start: 0,
//                 end: 100,
//               },
//               {
//                 type: 'inside',
//               },
//             ],
//             xAxis: {
//               data: dates,
//               type: 'category',
//               name: '日期',
//             },
//             yAxis: {
//               type: 'value',
//               min: Math.min(...stock.data.map((item) => item.收盘)),
//               max: Math.max(...stock.data.map((item) => item.收盘)),
//               name: '收盘价',
//             },
//             series: [
//               {
//                 name: '收盘价',
//                 type: 'line',
//                 data: stock.data.map((item) => item.收盘),
//               },
//             ],
//           })
</script>

<style lang="scss" scoped></style>
