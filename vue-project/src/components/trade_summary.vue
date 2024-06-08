<template>
  <el-row>
    <el-col :span="12">
      <el-card style="max-width: 480px; margin-bottom: 20px">
        <template #header>
          <div class="card-header">
            <span>
              <h1>策略概览</h1>
            </span>
          </div>
        </template>
        <div class="number-display">
    <div class="main-number" :style="{ color: compare.today - compare.yesterday > 0 ? 'red' : 'green' }">
      {{ compare.today - compare.yesterday }}
      <el-icon class="icon">
        <template v-if="compare.today - compare.yesterday > 0">
          <Top /> <!-- 上升箭头 -->
        </template>
        <template v-else>
          <Bottom /> <!-- 下降箭头 -->
        </template>
      </el-icon>
    </div>
    <div class="sub-number" :style="{ color: compare.today - compare.yesterday > 0 ? 'red' : 'green' }">
      {{ compare.percent.toFixed(2) }}%
    </div>
  </div>
        （总资产=持股+现金）
        <el-form ref="formRef" label-width="auto" style="margin-top: 15px;">
          <el-form-item label="今日总资产" prop="name">{{
            compare.today
          }}</el-form-item>
          <el-form-item label="昨日总资产" prop="zone">{{
            compare.yesterday
          }}</el-form-item>
          <el-form-item label="涨跌额" prop="zone">{{
            compare.today - compare.yesterday
          }}</el-form-item>
          <el-form-item label="涨跌幅(%)" prop="zone">{{
            compare.percent.toFixed(2)
          }}</el-form-item>
        </el-form>
        <!-- 根据用户的涨跌幅情况选择不同的评论 -->
        {{ userComment }}
      </el-card>
    </el-col>
    <el-col :span="12">
      <div class="grid-content ep-bg-purple-light">
        <h1>持仓总结</h1>
        <div ref="chartRef" style="width: 600px; height: 400px" v-loading="isLoading"></div>
        <h2 style="margin-top: 15px">前五大持仓</h2>
      </div>
      <div>
        <el-table :data="topfive" stripe style="width: 100%">
          <el-table-column fixed prop="0" label="股票代码" />
          <el-table-column prop="1.0" label="股票名称" />
          <el-table-column prop="1.1" label="单股价格" />
          <el-table-column prop="1.2" label="持有数量" />
          <el-table-column prop="1.3" label="总价值" sortable />
        </el-table>
      </div>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import * as echarts from 'echarts'
import { useStorage } from '@vueuse/core'
import axios from 'axios' // 导入 axios 库，用于发送 HTTP 请求
const user = useStorage('user', {
  name: '',
  remember: false,
  password: '',
  account: '',
  balance: 1000000,
  all_property: 0,
  stocks_held: undefined,
})
const comment = ref([
  '恭喜你，你的股票涨幅很大，继续保持！',//涨幅很大，赞美用户
  '你的股票有所上涨，继续努力！', //略有涨幅，鼓励用户
  '你的股票有些亏损，别灰心。市场瞬息万变，不妨试试我们的量化策略？', //略有亏损，安慰用户
  '你的股票亏损较大，注意风险，适时调整策略。', //大量亏损，警示用户
])
const userComment = computed(() => {
  const percent = compare.value.percent;
  console.log(percent)
  if (percent > 3) {
    return comment.value[0]; // 涨幅很大，赞美用户
  } else if (percent > 0) {
    return comment.value[1]; // 略有涨幅，鼓励用户
  } else if (percent > -3) {
    return comment.value[2]; // 略有亏损，安慰用户
  } else {
    return comment.value[3]; // 大量亏损，警示用户
  }
});

const chartRef = ref(null)
const all_property = reactive({
  //理论上，应该由后端根据用户持股来转换，而不是我在这里写死
  A股: 1000,
  美股: 500,
  港股: 200,
})
const total = computed(() =>
  Object.values(all_property).reduce((a, b) => a + b, 0)
)

const topfive = useStorage('topfive', [])
topfive.value = []
const compare = useStorage('compare', {
  today: 0,
  yesterday: 0,
  percent: 0,
})
const isLoading = computed(() => topfive.value.length === 0);
async function get_compare() { //获取今日和昨日总资产的价值
  const path = 'http://localhost:5000/home/today-and-yesterday'
  try {
    const res = await axios.post(path, user.value)
    if (res.data.status === 'success') {
      compare.value.today = res.data.today
      compare.value.yesterday = res.data.yesterday
      compare.value.percent = res.data.change
      console.log('获取今日和昨日总资产的价值成功')
    } else {
      console.error('获取今日和昨日总资产的价值失败')
    }
  } catch (error) {
    console.error(error)
    console.error('网络问题，获取今日和昨日总资产的价值失败，请重试')
  }
}
async function get_topfive() {
  // 获取前五大持仓
  const path = 'http://localhost:5000/home/topFive'
  try {
    const res = await axios.post(path, user.value)
    if (res.data.status === 'success') {
      topfive.value = res.data.topFive
      console.log('获取前五大持仓成功')
      console.log(topfive.value)
    } else {
      console.error('获取前五大持仓失败')
    }
  } catch (error) {
    console.error(error)
    console.error('网络问题，获取前五大持仓失败，请重试')
  }
}
onMounted(async () => {
  // await get_compare()
  await get_topfive()
  console.log(chartRef.value);
  const chart = echarts.init(chartRef.value)
  console.log(topfive.value);
  // const data = Object.entries(all_property).map(([name, value]) => ({ name, value }));
  const data = topfive.value.map(([_code, info]) => ({
    name: info[0],
    value: Math.floor(Number(info[3])),
  })) // 使用 '股票名称' 作为名称，'总价值' 作为值
  console.log(data);
  chart.setOption({
    title: {
      text: '资产分布',
      left: 'center',
    },
    series: [
      {
        type: 'pie',
        data: data,
        electedMode: 'single', // 允许用户通过点击来选中部分
        selectedOffset: 30, // 选中部分被拉出的距离
        label: {
          formatter: '{b}: {c} \n ({d}%)',
        },
      },
    ],
  })
})
</script>

<style lang="scss" scoped>
h1 {
  font-size: 24px;
}

h2 {
  font-size: 20px;
}
.number-display {
  text-align: center;
}

.main-number {
  font-size: 2em;
  font-weight: bold;
}

.icon {
  
  margin-left: 0.2em;
}

.sub-number {
  font-size: 1em;
}
</style>
