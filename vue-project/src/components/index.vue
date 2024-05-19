<!-- 首页 -->
<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <!-- <div class="image1">
                    <el-image style="width: 15px; height: 75px" src="../assets/艺术字.png" fit="contain" />
                </div> 
                离谱，加了这个图片不能正常显示，而且退出登录好像也不能用了 -->
                
                <div class="welcome-message">欢迎您:{{ user.name }} 
                    <el-button type="primary" @click="handleLogout" plain>退出登录</el-button>
                </div>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <h5 class="mb-2"></h5>
                    <el-menu default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
                        <el-sub-menu index="1">
                            <template #title>
                                <el-icon>
                                    <location />
                                </el-icon>
                                <span>实时行情</span>
                            </template>
                            <el-menu-item-group title="股市">
                                <el-menu-item index="1-1" @click="switch_SH">国内市场</el-menu-item>
                                <el-menu-item index="1-2">国际市场</el-menu-item>
                            </el-menu-item-group>
                            <el-menu-item-group title="期货">
                                <el-menu-item index="1-3">item three</el-menu-item>
                            </el-menu-item-group>
                            <el-menu-item-group title="汇率">
                                <el-sub-menu index="1-4">
                                    <template #title>item four</template>
                                    <el-menu-item index="1-4-1">item one</el-menu-item>
                                </el-sub-menu>
                            </el-menu-item-group>
                        </el-sub-menu>

                        <el-menu-item index="2" @click="switch1">
                            <el-icon><icon-menu /></el-icon>

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