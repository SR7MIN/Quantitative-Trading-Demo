<!-- 首页 -->
<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div class="image1">
          <!-- <el-image style="width: 15px; height: 75px" src="../assets/艺术字.png" fit="contain" /> -->
          <img
            src="../assets/艺术字.png"
            alt="艺术字"
            class="image"
            style="width: 180px; position: relative; top: 5px"
          />
          <span class="welcome-message"
            >欢迎您:{{ user.name }}
            <el-button type="primary" @click="handleLogout" plain
              >退出登录</el-button
            >
          </span>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <!-- <h5 class="mb-2">aaa</h5> -->
          <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
            <el-radio-button :value="false">展开侧栏</el-radio-button>
            <el-radio-button :value="true">收起侧栏</el-radio-button>
          </el-radio-group>
          <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            active-text-color="#ffd04b"
            background-color="#545c64"
            text-color="#fff"
            @open="handleOpen"
            @close="handleClose"
          >
            <el-sub-menu index="1">
              <template #title>
                <el-icon>
                  <TrendCharts />
                </el-icon>
                <span>实时行情</span>
              </template>
              <el-menu-item-group title="股市">
                <el-menu-item index="1-1" @click="switch_SH"
                  >国内市场</el-menu-item
                >
                <el-menu-item index="1-2" @click="switch_internation"
                  >国际市场</el-menu-item
                >
              </el-menu-item-group>
              <!-- <el-menu-item-group title="期货">
                <el-menu-item index="1-3" @click="switch_feature"
                  >期货市场</el-menu-item
                >
              </el-menu-item-group> -->
              <el-menu-item-group title="汇率">
                <el-menu-item index="1-4" @click="switch_exchange_rate"
                  >汇率市场</el-menu-item
                >
              </el-menu-item-group>
            </el-sub-menu>
            <el-sub-menu index="5">
              <template #title>
                <el-icon>
                  <Shop />
                </el-icon>
                <span>模拟交易</span>
              </template>
              <el-menu-item index="5-1" @click="switch_trade_summary"
                >历史总结</el-menu-item
              >
              <el-menu-item index="5-2" @click="switch_trade_do"
                >执行交易</el-menu-item
              >
              <el-menu-item index="5-3" @click="switch_trade_analyze"
                >盈亏分析</el-menu-item
              >
            </el-sub-menu>

            <el-menu-item index="2" @click="switch1">
              <el-icon>
                <MagicStick />
              </el-icon>

              <span>量化策略</span>
            </el-menu-item>
            <el-menu-item index="3" @click="switch2">
              <el-icon>
                <document />
              </el-icon>
              <span>风险管理</span>
            </el-menu-item>
            <el-menu-item index="4" @click="switch3">
              <el-icon>
                <setting />
              </el-icon>
              <span>个性设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { get, useStorage } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'
const route = useRouter()
const isCollapse = ref(false)
const handleLogout = () => {
  user.value = null
  topfive.value = []
  compare.value = {
    today: 0,
    yesterday: 0,
    percent: 0,
  }
  route.push('/login')
}
const user = useStorage('user', {
  name: '',
  remember: false,
  password: '',
  account: '',
  balance: 1000000,
  all_property: 0,
  stocks_held: undefined,
})
const compare = useStorage('compare',{
  today: 0,
  yesterday: 0,
  percent: 0,
})
const topfive = useStorage('topfive', [])
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
async function get_compare(){ //获取今日和昨日总资产的价值
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
async function get_all_property() {
  const path = 'http://localhost:5000/home/total'
  try {
    const res = await axios.post(path, user.value)
    if (res.data.status === 'success') {
      user.value.all_property = res.data.total
      console.log('获取用户所有资产成功')
      console.log(user.value.all_property)
    } else {
      console.error('获取用户所有资产失败')
    }
  } catch (error) {
    console.error(error)
    console.error('网络问题，获取用户所有资产失败，请重试')
  }
}
onMounted(() => {
  get_all_property()
  get_topfive()
  get_compare()
})
// onMounted(async () => {
//     try {
//         user.value = useStorage('user', ({
//             name: '',
//             remember: false,
//             password: '',
//             account: '',
//             balance: 1000000,
//             stocks_held: undefined,
//         }));
//     } catch (error) {
//         console.error(error);
//     }
// });
if (!user.value.name) {
  route.push('/login')
}
function switch1() {
  //跳转到量化策略页面
  route.push('/index/strategy')
}
function switch2() {
  //跳转到风险管理页面
  route.push('/index/manage')
}
function switch3() {
  //跳转到个性设置页面
  route.push('/index/setting')
}
function switch_SH() {
  //跳转到上证指数页面
  route.push('/index/shanghai')
}
function switch_internation() {
  //跳转到国际股票市场页面
  route.push('/index/internation')
}
function switch_feature() {
  //跳转到期货市场页面
  route.push('/index/feature')
}
function switch_exchange_rate() {
  //跳转到汇率市场页面
  route.push('/index/exchange_rate')
}
function switch_trade_summary() {
  //跳转到模拟交易总结页面
  route.push('/index/trade_summary')
}
function switch_trade_do() {
  //跳转到模拟交易执行页面
  route.push('/index/trade_do')
}
function switch_trade_analyze() {
  //跳转到模拟交易盈亏分析页面
  route.push('/index/trade_analyze')
}
</script>

<style lang="scss" scoped>
.welcome-message {
  float: right;
}

.common-layout {
  .mb-2 {
    text-align: center;
  }
}
</style>
