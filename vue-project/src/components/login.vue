<template>
    <div class="container">
        <img src="../assets/logo.png" alt="Your Image" class="image">
    </div>
    <div class="login_container">
        <div class="login_form">
            <p1>量化交易平台-登录界面</p1>
            <el-form ref="formRef" :model="form" :rules="rules" label-width="auto">
                <el-form-item label="" prop="account">
                    <el-input v-model="form.account" 
                    placeholder="请输入账号" :prefix-icon="User" />
                </el-form-item>
                <el-form-item label="" prop="password">
                    <el-input v-model="form.password" style="width: 240px" 
                     type="password" placeholder="请输入密码"
                        show-password :prefix-icon="Lock" />
                </el-form-item>
                <div class="text">
                    <el-checkbox v-model="form.remember" label="记住密码" size="large" />
                    <el-text class="mx-1" type="primary">忘记密码？</el-text>
                </div>
                <div class="button-container">
                    <el-button type="primary" @click="handle_login">登录</el-button>
                </div>
                <div class="signup-link">
                    <el-text class="mx-1">还没有账号？</el-text>
                    <el-link type="primary" @click="handle_signup">去注册</el-link>
                </div>
            </el-form>

            <el-divider content-position="center">其他登录方式</el-divider>

        </div>
    </div>
</template>

<script setup>

// import { User } from '@element-plus/icons-vue/dist/types';
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue';
import { ref } from 'vue';
import axios from 'axios';
import { useStorage } from '@vueuse/core';


const router = useRouter();

function handle_login() {
    form.value.name = '测试用户一号';
    ElMessage.success('登录成功');
    router.push("/index");
};

function handle_signup() {
    router.push('/sign_up');
};

const form = useStorage('user', ({ //实际上 form应该写成user
    name: '',
    remember: false,
    password: '',
    account: '',
}));

if (form.value.name) {
    handle_login()
}
const rules = reactive({
    password: [
        { validator: validatePassword, trigger: 'blur' }
    ],
    account: [
        { validator: validateaccount, trigger: 'blur' }],

    // 其他字段的验证规则
});
function validateaccount(rule, value, callback) {
    const pattern = /^[0-9]{6,10}$/;
    if (!pattern.test(value)) {
        callback(new Error('账号应为6-10位的数字'));
    } else {
        callback();
    }
}
function validatePassword(rule, value, callback) {
    const pattern = /^[a-zA-Z0-9.,!@#$%^&*()]{3,10}$/;
    if (!pattern.test(value)) {
        callback(new Error('密码应为3-10位的数字、字母和标点的组合'));
    } else {
        callback();
    }
}


// async function handle_login() {
//     const path = 'http://localhost:5000/login';
//     try {
//         const res = await axios.post(path, form.value);
//         if (res.data.success) {
//             ElMessage.success('登录成功');
//             router.push('/index');
//             form.value = res.data.user
//         } else {
//             // handle login failure
//             console.error('Login failed');
//             ElMessage.error('登录失败，请重试');
//         }
//     } catch (error) {
//         console.error(error);
//         ElMessage.error('登录失败，请重试222');
//     }
// }

</script>

<style lang="scss" scoped>
.image {
    width: 160px;
    /* 设置图片宽度 */
    height: auto;
    /* 根据宽度自动调整高度 */
    position: absolute;
    /* 设定图片的定位方式为绝对定位 */
    left: 50%;
    /* 设置图片距离左侧的位置 */
    transform: translateX(-50%);
    /* 添加这里 */
}

.login_container {
    // background-image: url('../assets/bg_image/logo.png');
    height: 100vh;
    display: flex;
    justify-content: center;
    /* 修改这里 */
    background-size: cover;
    background-position: left;

    .login_form {
        width: 50%;
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 20px;
        /* 添加这里 */
    }

    p1 {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    .text {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .el-form-item {
        margin-bottom: 15px;
    }

    .el-input {
        width: 100%;
    }

    .el-checkbox {
        margin: 10px 0;
    }

    .el-button {
        width: 100%;
        margin-top: 10px;
    }

    .signup-link {
        margin-top: 10px;
        text-align: center;
    }
}
</style>