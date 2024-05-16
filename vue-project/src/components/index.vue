<!-- 首页 -->
<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                搜索栏、用户设置等
                <span class="welcome-message">欢迎您:{{ user.name }}</span>
                <el-button type="text" @click="handleLogout">退出登录</el-button>
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
                            <el-menu-item-group title="国内市场">
                                <el-menu-item index="1-1">上证指数</el-menu-item>
                                <el-menu-item index="1-2">深证成指</el-menu-item>
                            </el-menu-item-group>
                            <el-menu-item-group title="国际市场">
                                <el-menu-item index="1-3">item three</el-menu-item>
                            </el-menu-item-group>
                            <el-sub-menu index="1-4">
                                <template #title>item four</template>
                                <el-menu-item index="1-4-1">item one</el-menu-item>
                            </el-sub-menu>
                        </el-sub-menu>
                        <el-menu-item index="2">
                            <el-icon><icon-menu /></el-icon>
                            <span>量化策略</span>
                        </el-menu-item>
                        <el-menu-item index="3">
                            <el-icon>
                                <document />
                            </el-icon>
                            <span>风险管理</span>
                        </el-menu-item>
                        <el-menu-item index="4">
                            <el-icon>
                                <setting />
                            </el-icon>
                            <span>个性设置</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main>主展示页面</el-main>
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
const user =useStorage('user',({ //实际上 form应该写成user
    name: '',
    remember: false,
    password: '',
    account: '',
}));

if(! user.value.name) {
    route.push('/login');
}

console.log(user);
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