<!-- 首页 -->
<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <div class="image1">
                    <!-- <el-image style="width: 15px; height: 75px" src="../assets/艺术字.png" fit="contain" /> -->
                    <img src="../assets/艺术字.png" alt="艺术字" class="image"
                        style="width: 180px; position: relative; top: 5px;" />
                    <span class="welcome-message">欢迎您:{{ user.name }}
                        <el-button type="primary" @click="handleLogout" plain>退出登录</el-button>
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
                    <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="isCollapse"
                        active-text-color="#ffd04b" background-color="#545c64" text-color="#fff" 
                        @open="handleOpen" @close="handleClose">
                        <el-sub-menu index="1">
                            <template #title>
                                <el-icon>
                                    <TrendCharts />
                                </el-icon>
                                <span>实时行情</span>
                            </template>
                            <el-menu-item-group title="股市">
                                <el-menu-item index="1-1" @click="switch_SH">国内市场</el-menu-item>
                                <el-menu-item index="1-2" @click="switch_internation">国际市场</el-menu-item>
                            </el-menu-item-group>
                            <el-menu-item-group title="期货">
                                <el-menu-item index="1-3" @click="switch_feature">期货市场</el-menu-item>
                            </el-menu-item-group>
                            <el-menu-item-group title="汇率">

                                <el-menu-item index="1-4" @click="switch_exchange_rate">汇率市场</el-menu-item>

                            </el-menu-item-group>
                        </el-sub-menu>
                        <el-sub-menu index="5">
                            <template #title>
                                <el-icon>
                                    <Shop />
                                </el-icon>
                                <span>模拟交易</span>
                            </template>
                            <el-menu-item index="5-1" @click="switch_trade_summary">历史总结</el-menu-item>
                            <el-menu-item index="5-2" @click="switch_trade_do">执行交易</el-menu-item>
                            <el-menu-item index="5-3" @click="switch_trade_analyze">盈亏分析</el-menu-item>
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
                    <div>主展示页面</div>
                    <RouterView />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup>
import { useStorage } from '@vueuse/core';
import { useRouter } from 'vue-router';
const route = useRouter();
const isCollapse = ref(true);
const handleLogout = () => {
    user.value = null;
    route.push('/login');
};
const user = useStorage('user', ({ //实际上 form应该写成user
    name: '',
    remember: false,
    password: '',
    account: '',
}));

if (!user.value.name) {
    route.push('/login');
}
function switch1() { //跳转到量化策略页面
    route.push('/index/strategy');
}
function switch2() { //跳转到风险管理页面
    route.push('/index/manage');
}
function switch3() { //跳转到个性设置页面
    route.push('/index/setting');
}
function switch_SH() { //跳转到上证指数页面
    route.push('/index/shanghai');
}
function switch_internation() { //跳转到国际股票市场页面
    route.push('/index/internation');
}
function switch_feature() { //跳转到期货市场页面
    route.push('/index/feature');
}
function switch_exchange_rate() { //跳转到汇率市场页面
    route.push('/index/exchange_rate');
}
function switch_trade_summary() { //跳转到模拟交易总结页面
    route.push('/index/trade_summary');
}
function switch_trade_do() { //跳转到模拟交易执行页面
    route.push('/index/trade_do');
}
function switch_trade_analyze() { //跳转到模拟交易盈亏分析页面
    route.push('/index/trade_analyze');
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