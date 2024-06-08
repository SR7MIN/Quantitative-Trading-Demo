<template>
  <div style="margin-top: 15px; display: flex; justify-content: space-between">
    <div>
      可查询港股的全部股票信息
      <el-button type="primary" @click="Search_stock">
        <el-icon>
          <Search />
        </el-icon>
        股票查询
      </el-button>
      （今日推荐股票：{{ good_stock[0]}} ）
    </div>
    <div>
      <el-button type="success" @click="dialog = true" v-show="stockQueried">
        买入
      </el-button>
      <el-drawer
        v-model="dialog"
        title="请输入您的交易信息"
        :before-close="handleClose"
        direction="rtl"
        class="demo-drawer1"
      >
        <div class="demo-drawer__content">
          <el-form :model="form">
            <el-form-item label="选购股数" :label-width="formLabelWidth">
              <el-input v-model="form.num" autocomplete="off" />
            </el-form-item>
            <el-form-item label="总价格" :label-width="formLabelWidth">
              {{ totalOutcome }}
            </el-form-item>
          </el-form>
          <div class="demo-drawer__footer">
            <el-button @click="cancelForm">取消交易</el-button>
            <el-button type="primary" :loading="loading" @click="onClick">
              {{ loading ? 'Submitting ...' : '提交交易' }}
            </el-button>
          </div>
        </div>
      </el-drawer>
      <el-button type="danger" @click="dialog2 = true" v-show="stockQueried">
        卖出
      </el-button>
      <el-drawer
        v-model="dialog2"
        title="请输入您的交易信息"
        :before-close="handleClose"
        direction="rtl"
        class="demo-drawer"
      >
        <!-- :append-to-body="true" -->
        <div class="demo-drawer__content">
          <el-form :model="form">
            <el-form-item label="卖出股数" :label-width="formLabelWidth">
              <el-input v-model="form.num" autocomplete="off" />
            </el-form-item>
            <el-form-item label="总收益" :label-width="formLabelWidth">
              {{ totalIncome }}
            </el-form-item>
          </el-form>
          <div class="demo-drawer__footer">
            <el-button @click="cancelForm">取消交易</el-button>
            <el-button type="primary" :loading="loading" @click="onClick2">
              {{ loading ? 'Submitting ...' : '提交交易' }}
            </el-button>
          </div>
        </div>
      </el-drawer>
    </div>
  </div>
  <div>
    <el-row>
      <el-col :span="12">
        <div class="grid-content ep-bg-purple" />
        <div ref="chartRef" style="width: 600px; height: 400px"></div>
      </el-col>
      <el-col :span="12">
        <div class="grid-content ep-bg-purple-light" />
        <div ref="chartRef2" style="width: 600px; height: 400px"></div>
      </el-col>
    </el-row>
    <div>
      <h1>近五日交易详细信息</h1>
    </div>
    <el-table :data="recentData.value" stripe style="width: 100%">
      <el-table-column
        prop="日期"
        label="日期"
        :formatter="(row) => new Date(row.日期).toLocaleDateString()"
      />
      <el-table-column prop="开盘" label="开盘" />
      <el-table-column prop="收盘" label="收盘" />
      <el-table-column prop="最高" label="最高" />
      <el-table-column prop="最低" label="最低" />
      <el-table-column prop="成交量" label="成交量" />
      <!-- 成交额    振幅   涨跌幅   涨跌额   换手率 -->
      <el-table-column prop="成交额" label="成交额" />
      <el-table-column prop="振幅" label="振幅" />
      <el-table-column prop="涨跌幅" label="涨跌幅" />
      <el-table-column prop="涨跌额" label="涨跌额" />
      <el-table-column prop="换手率" label="换手率" />
    </el-table>
    <div>
      <h1>今日最新交易信息</h1>
      <el-table :data="todayData.value" stripe style="width: 100%">
        <el-table-column prop="代码" label="代码" />
        <el-table-column prop="名称" label="名称" />
        <el-table-column prop="最新价" label="最新价" />
        <el-table-column prop="成交量" label="成交量" />
        <el-table-column prop="成交额" label="成交额" />
        <el-table-column prop="今开" label="今开" />
        <el-table-column prop="昨收" label="昨收" />
        <el-table-column prop="最低" label="最低" />
        <el-table-column prop="最高" label="最高" />
        <el-table-column prop="涨跌幅" label="涨跌幅" />
        <el-table-column prop="涨跌额" label="涨跌额" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
// import { ElLoading, ElMessage, ElMessageBox } from 'element-plus';
import { onMounted } from 'vue'
import { useStorage } from '@vueuse/core'
let chart = null
let stockQueried = ref(false) //是否查询到了股票
const good_stock = ref([['00031','01058','00700']])
const chartRef = ref(null)
let chart2 = null
const chartRef2 = ref(null)
let recentData = reactive({
  //近五天历史数据
  value: [],
})
let todayData = reactive({
  value: [],
})
let recentData2 = reactive({
  //近60天历史数据，用来画K线图
  value: [],
  // 里面包括60天的日期 开盘 收盘 最高 最低 成交量 成交额 振幅 涨跌幅 涨跌额 换手率
})

const user = useStorage('user', {
  name: '',
  remember: false,
  password: '',
  account: '',
  balance: 1000000,
  all_property: 0,
  stocks_held: undefined,
})
const form = reactive({
  //记录想进行交易的股票信息
  code: '',
  place: '',
  num: 0,
  account: undefined,
  price: undefined,
})
let totalIncome = computed(() => form.num * form.price)
let totalOutcome = computed(() => form.num * form.price)
const dialog = ref(false) //买入弹窗
const dialog2 = ref(false) //卖出弹窗
const loading = ref(false)
const stock = reactive({
  //记录查询到的股票信息
  code: '',
  name: '',
  data: '',
})
const onClick = () => {
  buy_stock()
  loading.value = true
  setTimeout(() => {
    loading.value = false
    dialog.value = false
    dialog2.value = false
  }, 400)
}
const onClick2 = () => {
  sell_stock()
  loading.value = true
  setTimeout(() => {
    loading.value = false
    dialog.value = false
    dialog2.value = false
  }, 400)
}
async function sell_stock() {
  const path = 'http://localhost:5000/home/sell'
  form.code = stock.code
  form.account = user.value.account
  try {
    const res = await axios.post(path, form)
    if (res.data.status === 'success') {
      ElMessage.success('交易成功')
      user.value.balance = res.data.balance
    } else {
      ElMessage.error('交易失败，卖出的股票超过拥有量')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('网络问题，交易失败，请重试222')
  }
}
async function buy_stock() {
  // 购买
  const path = 'http://localhost:5000/home/buy'
  form.code = stock.code
  form.account = user.value.account
  try {
    const res = await axios.post(path, form)
    if (res.data.status === 'success') {
      ElMessage.success('交易成功')
      user.value.balance = res.data.balance
    } else {
      // handle login failure
      console.error('Login failed')
      ElMessage.error('交易失败，余额不足')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('网络问题，交易失败，请重试222')
  }
}
const handleClose = (done) => {
  if (loading.value) {
    return
  }
  ElMessageBox.confirm('强制退出会放弃此次交易，是否继续？', {
    confirmButtonText: '是',
    cancelButtonText: '否',
  })
    .then(() => {
      loading.value = false
      dialog.value = false
      dialog2.value = false
      clearTimeout(timer)
      form.code = ''
      form.place = ''
      form.num = undefined
      form.price = undefined
      done()
    })
    .catch(() => {
      // catch error
    })
}

const cancelForm = () => {
  loading.value = false
  dialog.value = false
  dialog2.value = false
  clearTimeout(timer)
  form.code = ''
  form.place = ''
  form.num = undefined
  form.price = undefined
}
const Search_stock = () => {
  const loading = ElLoading.service({
    lock: true,
    fullscreen: true,
    text: '正在查询中...',
  })
  ElMessageBox.prompt('请输入您要查询的股票代码', 'Tip', {
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
    inputPattern: /^\d{5}$/,
    inputErrorMessage: '无效代码',
  })
    .then(async ({ value }) => {
      try {
        const res = await axios.post('http://localhost:5000/home/HKstock', {
          code: value,
        })

        loading.close()
        if (res.data.status === 'succeed') {
          ElMessage({
            type: 'success',
            message: `股票查询成功！`,
          })
          stockQueried.value = true
          stock.code = value
          stock.name = res.data.stock_name
          stock.data = res.data.data
          recentData.value = stock.data.slice(-5)
          recentData2.value = stock.data.slice(-60)
          todayData.value = res.data.all_info
          console.log(todayData.value)
          form.price = todayData.value[0].最新价
          console.log(form.price)
          // 这里你可以处理response.data.data，它包含了股票数据

          // 使用ECharts绘制图表
          chart = echarts.init(chartRef.value)
          const dates = stock.data.map((item) => {
            const date = new Date(item.日期)
            return date.toLocaleDateString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
            })
          })
          chart.setOption({
            title: {
              text: `近一年历史股价 - ${stock.name}`,
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
              min: Math.min(...stock.data.map((item) => item.收盘)),
              max: Math.max(...stock.data.map((item) => item.收盘)),
              name: '收盘价',
            },
            series: [
              {
                name: '收盘价',
                type: 'line',
                data: stock.data.map((item) => item.收盘),
              },
            ],
          })
          chart2 = echarts.init(chartRef2.value)
          // const dates2 = recentData2.value.map(item => item.日期);
          const dates2 = recentData2.value.map((item) => {
            const date = new Date(item.日期)
            return date.toLocaleDateString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
            })
          })
          const data2 = recentData2.value.map((item) => [
            item.开盘,
            item.收盘,
            item.最低,
            item.最高,
          ])
          // 计算均线
          const maLine = data2.map((item, index, array) => {
            if (index < 5) {
              return '-'
            } else {
              let sum = 0
              for (let i = 0; i < 5; i++) {
                sum += array[index - i][1] // 收盘价
              }
              return (sum / 5).toFixed(2)
            }
          })
          const prices = data2.flat()
          const minPrice = Math.min(...prices)
          const maxPrice = Math.max(...prices)
          chart2.setOption({
            title: {
              text: `近60个交易日K线图`,
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
              },
            },
            xAxis: {
              data: dates2,
            },
            yAxis: {
              min: (minPrice - (maxPrice - minPrice) * 0.05).toFixed(2),
              max: (maxPrice + (maxPrice - minPrice) * 0.05).toFixed(2),
            },
            series: [
              {
                type: 'k',
                data: data2,
              },
              {
                type: 'line',
                data: maLine,
                smooth: true,
                lineStyle: {
                  normal: { opacity: 0.5 },
                },
                name: 'MA5',
              },
            ],
          })
        } else {
          ElMessage({
            type: 'error',
            message: '股票查询失败',
          })
        }
      } catch (error) {
        stockQueried.value = false
        loading.close()
        ElMessage({
          type: 'error',
          message: '查找失败',
        })
        console.log(error)
      }
    })
    .catch(() => {
      stockQueried.value = false
      loading.close()
      ElMessage({
        type: 'info',
        message: '操作取消',
      })
    })
}
</script>
<style lang="scss" scoped></style>
