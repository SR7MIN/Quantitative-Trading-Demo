<template>
    <div class="container">
        <img src="../assets/logo.png" alt="Your Image" class="image">
    </div>
    <div class="login_container">
        <div class="login_form">
            <p1>量化交易平台-注册界面</p1>
            <el-form ref="formRef" :model="form" :rules="rules" label-width="auto">
                <el-form-item label="">
                    <!-- 账号似乎系统分配更好？不应让用户输入？类似QQ号的注册方式 -->
                    <el-input v-model="form.account" placeholder="请输入账号" :prefix-icon="User" />
                </el-form-item>
                <el-form-item label="">
                    <el-input v-model="form.name" placeholder="请输入昵称" :prefix-icon="Avatar" />
                </el-form-item>
                <el-form-item label="" prop="password">
                    <el-input v-model="form.password" 
                    style="width: 240px" type="password" placeholder="请输入密码"
                    show-password :prefix-icon="Lock"/>    
                </el-form-item>
                <div class="button-container">
                    <el-button type="primary" @click="send_sign_up">注册</el-button>
                </div>
                <div class="login-link">
                    <el-text class="mx-1">已有账号？</el-text>
                    <el-link type="primary" @click="handle_login">去登录</el-link>
                </div>
            </el-form>
            <el-divider content-position="center">其他注册方式</el-divider>

        </div>
    </div>
</template>

<script setup>
// import { User } from '@element-plus/icons-vue/dist/types';
import { useRouter } from 'vue-router'
import { User, Lock, Avatar } from '@element-plus/icons-vue';
import { ref } from 'vue';
const form = ref({ //实际上 form应该写成user
    name: '',
    remember: false,
    password: '',
    account: '',
});

// 表单校验，GPT写的，好像不太对，但是我也不知道怎么改
const rules = reactive({
    password: [
        { validator: validatePassword, trigger: 'blur' }
    ],

    // 其他字段的验证规则
});

function validatePassword(rule, value, callback) {
    const pattern = /^[a-zA-Z0-9.,!@#$%^&*()]{3,10}$/;
    if (!pattern.test(value)) {
        callback(new Error('密码应为3-10位的数字、字母和标点的组合'));
    } else {
        callback();
    }
}

const router = useRouter();
function handle_login() {
    router.push('/login');
};

async function send_sign_up() {
    const path = 'http://localhost:5000/login';
    try {
        const res = await axios.post(path, form.value);
        if (res.data.success) {
            ElMessage.success('注册成功，请登录');
            router.push('/login');
        } else {
            // handle login failure
            console.error('Login failed');
            ElMessage.error('注册失败，请重试');
        }
    } catch (error) {
        console.error(error);
        ElMessage.error('网络问题，注册失败，请重试222');
    }
}

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

    .login-link {
        margin-top: 10px;
        text-align: center;
    }

}
</style>